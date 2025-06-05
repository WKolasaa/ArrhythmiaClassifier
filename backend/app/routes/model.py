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

bp = Blueprint("predict", __name__, url_prefix="/model")
MODEL_FOLDER = os.path.join(os.getcwd(), "model")  # Should point to backend/model/


@bp.route("/predict", methods=["POST"])
def predict():
    """
Make a prediction using a selected model and CSV input
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
    description: Bearer token
    default: "Bearer <your_token>"
  - name: model_name
    in: formData
    type: string
    required: true
    description: Name of the model (without .h5)
    example: best_model
  - name: file
    in: formData
    type: file
    required: true
    description: CSV file containing input features
responses:
  200:
    description: Prediction completed
    schema:
      type: object
      properties:
        message:
          type: string
          example: Prediction successful
        predictions:
          type: array
          items:
            type: integer
          example: [0, 1, 0, 2]
        model_used:
          type: string
          example: best_model
        confusion_matrix:
          type: array
          items:
            type: array
            items:
              type: integer
          example: [[10, 2], [1, 7]]
        accuracy:
          type: number
          example: 0.85
  400:
    description: Missing file or model name, or invalid file type
  401:
    description: Missing or invalid JWT token
  404:
    description: Model file not found
  500:
    description: Internal server error during prediction
"""
    # 1) Verify JWT token manually
    auth_header = request.headers.get("Authorization", None)
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid Authorization header"}), 401

    token = auth_header.split(" ")[1]
    payload = verify_token(token)
    if not payload:
        return jsonify({"error": "Invalid or expired token"}), 401

    user_id = payload.get("user_id")
    if user_id is None:
        return jsonify({"error": "Invalid token payload"}), 401

    # 2) Ensure model_name is provided
    model_name = request.form.get("model_name", None)
    if not model_name:
        return jsonify({"error": "Missing model_name in form data"}), 400

    # 3) Ensure file is provided
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename, {"csv"}):
        return jsonify({"error": "Invalid file type; only CSV allowed"}), 400

    # 4) Construct model path
    model_filename = f"{model_name}.h5"
    model_path = os.path.join(MODEL_FOLDER, model_filename)
    if not os.path.exists(model_path):
        return jsonify({"error": f"Model '{model_name}' not found"}), 404

    # 5) Save uploaded CSV to a temp location
    filename = secure_filename(file.filename)
    tmp_path = os.path.join("/tmp", filename)
    file.save(tmp_path)

    try:
        # 6) Load the chosen model
        model = tf.keras.models.load_model(model_path)

        # 7) Read CSV and prepare features (drop "label" column if present)
        data = pd.read_csv(tmp_path)
        X = data.drop(columns=["type"], errors="ignore").values

        # 8) Run inference
        predictions_proba = model.predict(X)
        predicted_labels = np.argmax(predictions_proba, axis=1).tolist()

        # 9) Save each prediction into the database
        for lab in predicted_labels:
            pred_record = Prediction(
                user_id=user_id,
                label=str(int(lab)),
                model_used=model_name
            )
            db.session.add(pred_record)
        db.session.commit()

        # 10) Build a simple confusion matrix / accuracy if labels provided
        response_payload = {
            "message": "Prediction successful",
            "predictions": predicted_labels,
            "model_used": model_name
        }

        # Optionally compute confusion matrix & accuracy if "type" column existed
        if "type" in data.columns:
            true_labels = data["type"].astype(int).tolist()
            from sklearn.metrics import confusion_matrix, accuracy_score
            cm = confusion_matrix(true_labels, predicted_labels).tolist()
            acc = accuracy_score(true_labels, predicted_labels)
            response_payload["confusion_matrix"] = cm
            response_payload["accuracy"] = acc

        return jsonify(response_payload), 200

    except Exception as e:
        # Clean up temp file, if desired: os.remove(tmp_path)
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
