import os
import pandas as pd
import numpy as np
import tensorflow as tf

from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models.prediction import Prediction
from app.models.user import User
from app.utils.files import allowed_file  
from app.utils.jwt import verify_token 
from sklearn.metrics import accuracy_score, confusion_matrix

from app.models.heartbeat import Heartbeat
from app.models.modelperformance import ModelPerformance
from app.models.patient import Patient

bp = Blueprint("predict", __name__, url_prefix="/model")
MODEL_FOLDER = os.path.join(os.getcwd(), "model")  # Should point to backend/model/
PREDICTION_LABELS = {
    0: "Normal",
    1: "Artial Premature",
    2: "Premature ventricular contraction",
    3: "Fusion of ventricular and normal",
    4: "Fusion of paced and normal"
}


@bp.route("/predict", methods=["POST"])
def predict():
    """
    Make a prediction using a selected model and ECG input data.

    ---
    tags:
      - Model
    consumes:
      - multipart/form-data
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Bearer JWT token (e.g., "Bearer YOUR_TOKEN")

      - name: model_name
        in: formData
        type: string
        required: true
        description: Name of the model without the .h5 extension

      - name: file
        in: formData
        type: file
        required: true
        description: >
          CSV file with ECG features per heartbeat. It must contain:
          "record" column (used as patient_id),
          and at least the following 32 columns:
          0_pre-RR to 1_qrs_morph4 (16 features × 2 timesteps).
          Optionally include a "type" column for ground truth labels.

    responses:
      200:
        description: Prediction successful
        schema:
          type: object
          properties:
            message:
              type: string
              example: Prediction successful
      400:
        description: Bad request (missing parameters or invalid file)
        schema:
          type: object
          properties:
            error:
              type: string
              example: Missing model_name in form data
      401:
        description: Unauthorized or invalid JWT
        schema:
          type: object
          properties:
            error:
              type: string
              example: Invalid or expired token
      404:
        description: Model not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: Model 'best_model' not found
      500:
        description: Internal server error
        schema:
          type: object
          properties:
            error:
              type: string
              example: Unexpected server error during prediction
    """
    try:
        user_id = authenticate_request()
        model_name, file, model_path = validate_input()
        tmp_path = save_uploaded_file(file)
        model, data = load_model_and_data(model_path, tmp_path)
        X, y_true = prepare_features(data)
        
        predictions_proba = model.predict(X)
        predicted_labels = np.argmax(predictions_proba, axis=1).tolist()

        accuracy = accuracy_score(y_true, predicted_labels) if y_true else None
        cm = confusion_matrix(y_true, predicted_labels).tolist() if y_true else None

        save_heartbeat_predictions(data, predicted_labels, predictions_proba, model_name)
        
        if y_true:
            save_model_performance(model_name, accuracy, cm)

        db.session.commit()

        return jsonify({"message": "Prediction successful"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/models", methods=["GET"])
def list_models():
    """
List available models for prediction
---
tags:
  - Model
parameters:
  - name: Authorization
    in: header
    type: string
    required: true
    description: Bearer token
    default: "Bearer <your_token>"
responses:
  200:
    description: List of available models
    schema:
      type: object
      properties:
        models:
          type: array
          items:
            type: string
          example: ["best_model", "cnn_model_v2"]
  401:
    description: Missing or invalid JWT token
"""
    auth_header = request.headers.get("Authorization", None)
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid Authorization header"}), 401

    token = auth_header.split(" ")[1]
    payload = verify_token(token)
    if not payload:
        return jsonify({"error": "Invalid or expired token"}), 401

    files = os.listdir(MODEL_FOLDER)
    model_names = [f[:-3] for f in files if f.endswith(".h5")]
    print("Model folder path:", MODEL_FOLDER)
    print("Files found:", os.listdir(MODEL_FOLDER))
    return jsonify({"models": model_names,}), 200

@bp.route("/model-performance/<int:id>", methods=["GET"])
def get_model_performance_by_id(id):
    """
    Get model performance record by ID
    ---
    tags:
      - ModelPerformance
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the model performance record
    responses:
      200:
        description: Model performance found
        schema:
          type: object
          properties:
            id:
              type: integer
            model_name:
              type: string
            accuracy:
              type: number
            confusion_matrix:
              type: array
            timestamp:
              type: string
      404:
        description: Model performance not found
    """
    perf = ModelPerformance.query.get(id)
    if not perf:
        return jsonify({"error": "Model performance not found"}), 404

    return jsonify({
        "id": perf.id,
        "model_name": perf.model_name,
        "accuracy": perf.accuracy,
        "confusion_matrix": perf.confusion_matrix, 
        "timestamp": perf.timestamp.isoformat() if perf.timestamp else None
    }), 200


@bp.route("/model-performance", methods=["GET"])
def list_model_performance_accuracies():
    """
    List accuracy values of all model performance records
    ---
    tags:
      - ModelPerformance
    responses:
      200:
        description: List of model accuracy entries
        schema:
          type: object
          properties:
            accuracies:
              type: array
              items:
                type: number
              example: [0.85, 0.91, 0.78]
    """
    performances = ModelPerformance.query.order_by(ModelPerformance.timestamp.desc()).all()
    accuracies = [{"id": p.id, "model": p.model_name, "accuracy": p.accuracy} for p in performances]
    return jsonify({"accuracies": accuracies}), 200

def authenticate_request():
    auth_header = request.headers.get("Authorization", None)
    if not auth_header or not auth_header.startswith("Bearer "):
        raise Exception("Missing or invalid Authorization header")
    token = auth_header.split(" ")[1]
    payload = verify_token(token)
    if not payload:
        raise Exception("Invalid or expired token")
    user_id = payload.get("user_id")
    if user_id is None:
        raise Exception("Invalid token payload")
    return user_id


def validate_input():
    model_name = request.form.get("model_name")
    if not model_name:
        raise Exception("Missing model_name in form data")
    if "file" not in request.files:
        raise Exception("No file part")
    file = request.files["file"]
    if file.filename == "":
        raise Exception("No selected file")
    if not allowed_file(file.filename, {"csv"}):
        raise Exception("Invalid file type; only CSV allowed")
    model_path = os.path.join(MODEL_FOLDER, f"{model_name}.h5")
    if not os.path.exists(model_path):
        raise Exception(f"Model '{model_name}' not found")
    return model_name, file, model_path


def save_uploaded_file(file):
    filename = secure_filename(file.filename)
    tmp_path = os.path.join("/tmp", filename)
    file.save(tmp_path)
    return tmp_path


def load_model_and_data(model_path, csv_path):
    model = tf.keras.models.load_model(model_path)
    data = pd.read_csv(csv_path)
    return model, data


def prepare_features(data):
    # Extract features (first 188 columns)
    X = data.iloc[:, :187].values

    # Use the last column as ground truth if available
    if data.shape[1] > 187:
        y_true = data.iloc[:, 187].tolist()
    else:
        y_true = None

    return X, y_true


def ensure_patient_exists(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        patient = Patient(id=patient_id, name="tmp")
        db.session.add(patient)
        db.session.flush()
    return patient


def save_heartbeat_predictions(data, predicted_labels, predictions_proba, model_name):
    try:
        for idx, row in data.iterrows():
          #patient_id = int(row["record"])
          #patient_id = 1 # For testing purposes, using a fixed patient_id
          patient_id = row[188]
          ensure_patient_exists(patient_id)

          ecg_vector = row.drop(labels=["record", "type"], errors="ignore").tolist()

          heartbeat = Heartbeat(
              patient_id=patient_id,
              ecg_features=ecg_vector,
              heartbeat_type=int(row[187]),
              predicted_type=PREDICTION_LABELS.get(predicted_labels[idx], "Unknown"),
              prediction_confidence=float(np.max(predictions_proba[idx])),
              model_name=model_name  
          )
        db.session.add(heartbeat)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def save_model_performance(model_name, accuracy, cm):
    performance = ModelPerformance(
        model_name=model_name,
        accuracy=accuracy,
        confusion_matrix=cm
    )
    db.session.add(performance)
