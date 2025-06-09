from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.patient import Patient
from datetime import datetime
from app.models.heartbeat import Heartbeat
from sqlalchemy import desc
import traceback
import io
import csv
from werkzeug.utils import secure_filename
from collections import Counter


bp = Blueprint('patients', __name__, url_prefix='/patients')


@bp.route('', methods=['POST'])
def create_patient():
    """
        Create a new patient
        ---
        tags:
          - Patients
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              required:
                - name
              properties:
                name:
                  type: string
                gender:
                  type: string
                  enum: [Male, Female, Other, Unknown]
                birth_date:
                  type: string
                  format: date
                  example: 1980-01-01
                contact_info:
                  type: string
        responses:
          201:
            description: Patient created successfully
          400:
            description: Missing required fields
          500:
            description: Server error
    """
    try:
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({"error": "Missing required fields"}), 400

        name = data['name']
        gender = data.get('gender')
        birth_date = data.get('birth_date')
        contact_info = data.get('contact_info')

        birth_date_parsed = datetime.strptime(birth_date, '%Y-%m-%d').date() if birth_date else None

        patient = Patient(
            name=name,
            gender=gender,
            birth_date=birth_date_parsed,
            contact_info=contact_info
        )
        db.session.add(patient)
        db.session.commit()

        return jsonify({
            "message": "Patient created successfully",
            "patient_id": patient.id
        }), 201

    except Exception as e:
        print(f"Patient creation error: {e}")
        return jsonify({"error": "Internal server error"}), 500



@bp.route('', methods=['GET'])
def list_patients():
    try:
        patients = Patient.query.all()
        result = []
        for p in patients:
            heartbeats = Heartbeat.query.filter_by(patient_id=p.id).all()
            prediction_types = [hb.predicted_type for hb in heartbeats if hb.predicted_type]

            if prediction_types:
                most_common_prediction = Counter(prediction_types).most_common(1)[0][0]
            else:
                most_common_prediction = None

            result.append({
                'id': p.id,
                'name': p.name,
                'gender': p.gender,
                'birth_date': p.birth_date.strftime('%Y-%m-%d') if p.birth_date else None,
                'contact_info': p.contact_info,
                'created_at': p.created_at.isoformat(),
                'most_common_prediction': most_common_prediction
            })

        return jsonify(result), 200

    except Exception as e:
        print(f"Error listing patients: {e}")
        return jsonify({"error": "Internal server error"}), 500




@bp.route('/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    """
        Get a specific patient by ID
        ---
        tags:
          - Patients
        parameters:
          - name: patient_id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Patient data
            schema:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                gender:
                  type: string
                birth_date:
                  type: string
                contact_info:
                  type: string
                created_at:
                  type: string
          404:
            description: Patient not found
    """
    patient = Patient.query.get(patient_id)

    if not patient:
        return jsonify({'error': 'Patient not found'}), 404

    return jsonify({
        'id': patient.id,
        'name': patient.name,
        'gender': patient.gender,
        'birth_date': patient.birth_date.strftime('%Y-%m-%d') if patient.birth_date else None,
        'contact_info': patient.contact_info,
        'created_at': patient.created_at.isoformat()
    }), 200
from app.models.heartbeat import Heartbeat


@bp.route('/<int:patient_id>/status', methods=['GET'])
def get_patient_status(patient_id):
    """
        Get arrhythmia status for a specific patient
        ---
        tags:
          - Patients
        parameters:
          - name: patient_id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Patient arrhythmia status
          404:
            description: Patient or heartbeats not found
    """
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404

    heartbeats = Heartbeat.query.filter_by(patient_id=patient_id).all()
    if not heartbeats:
        return jsonify({'error': 'No heartbeat data for this patient'}), 404

    abnormal_count = sum(1 for hb in heartbeats if hb.predicted_type == 'Arrhythmic')
    total = len(heartbeats)
    status = 'Arrhythmic' if abnormal_count > 0 else 'Normal'

    return jsonify({
        'patient_id': patient.id,
        'status': status,
        'total_heartbeats': total,
        'abnormal_heartbeats': abnormal_count
    }), 200


@bp.route('/<int:patient_id>/heartbeats', methods=['GET'])
def get_patient_heartbeats(patient_id):
    """
        Get all heartbeats for a patient
        ---
        tags:
          - Heartbeats
        parameters:
          - name: patient_id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: List of heartbeats with features and prediction
          404:
            description: Patient not found
    """
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404

    heartbeats = Heartbeat.query.filter_by(patient_id=patient_id).all()

    data = []
    for hb in heartbeats:
        data.append({
            'id': hb.id,
            'timestamp': hb.timestamp.isoformat(),
            'pre_RR': hb.pre_RR,
            'post_RR': hb.post_RR,
            'p_peak': hb.p_peak,
            't_peak': hb.t_peak,
            'r_peak': hb.r_peak,
            's_peak': hb.s_peak,
            'q_peak': hb.q_peak,
            'qrs_interval': hb.qrs_interval,
            'pq_interval': hb.pq_interval,
            'qt_interval': hb.qt_interval,
            'st_interval': hb.st_interval,
            'qrs_morph0': hb.qrs_morph0,
            'qrs_morph1': hb.qrs_morph1,
            'qrs_morph2': hb.qrs_morph2,
            'qrs_morph3': hb.qrs_morph3,
            'qrs_morph4': hb.qrs_morph4,
            'heartbeat_type': hb.heartbeat_type,
            'predicted_type': hb.predicted_type,
            'prediction_confidence': hb.prediction_confidence
        })

    return jsonify(data), 200
@bp.route('/<int:patient_id>/heartbeats/<int:heartbeat_id>', methods=['GET'])
def get_heartbeat_by_id(patient_id, heartbeat_id):
  """
        Get a specific heartbeat by ID for a patient
        ---
        tags:
          - Heartbeats
        parameters:
          - name: patient_id
            in: path
            type: integer
            required: true
          - name: heartbeat_id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Specific heartbeat data
          404:
            description: Patient or heartbeat not found
    """

  patient = Patient.query.get(patient_id)
  if not patient:
      return jsonify({'error': 'Patient not found'}), 404,

  heartbeat = Heartbeat.query.filter_by(id=heartbeat_id, patient_id=patient_id).first()
  if not heartbeat:
      return jsonify({'error': 'Heartbeat not found for this patient'}), 404

  data = {
          'id': heartbeat.id,
          'timestamp': heartbeat.timestamp.isoformat(),
          'pre_RR': heartbeat.pre_RR,
          'post_RR': heartbeat.post_RR,
          'p_peak': heartbeat.p_peak,
          't_peak': heartbeat.t_peak,
          'r_peak': heartbeat.r_peak,
          's_peak': heartbeat.s_peak,
          'q_peak': heartbeat.q_peak,
          'qrs_interval': heartbeat.qrs_interval,
          'pq_interval': heartbeat.pq_interval,
          'qt_interval': heartbeat.qt_interval,
          'st_interval': heartbeat.st_interval,
          'qrs_morph0': heartbeat.qrs_morph0,
          'qrs_morph1': heartbeat.qrs_morph1,
          'qrs_morph2': heartbeat.qrs_morph2,
          'qrs_morph3': heartbeat.qrs_morph3,
          'qrs_morph4': heartbeat.qrs_morph4,
          'heartbeat_type': heartbeat.heartbeat_type,
          'predicted_type': heartbeat.predicted_type,
          'prediction_confidence': heartbeat.prediction_confidence
  }

  return jsonify(data), 200
@bp.route('/stats', methods=['GET'])
def get_dashboard_stats():
    """
    Get dashboard statistics: total patients, classified arrhythmias, total arrhythmias
    """
    try:
        total_patients = Patient.query.count()
        total_arrhythmias = Heartbeat.query.count()

      
        classified_arrhythmias = Heartbeat.query.filter(
            Heartbeat.predicted_type.in_(["3", "Arrhythmic"])
        ).count()

        return jsonify({
            'total_patients': total_patients,
            'total_arrhythmias': total_arrhythmias,
            'classified_arrhythmias': classified_arrhythmias
        }), 200
    except Exception as e:
        print(f"Stats error: {e}")
        return jsonify({'error': 'Failed to get stats'}), 500
@bp.route('/bulk-upload', methods=['POST'])
def bulk_upload_patients():
    """
    Upload multiple patients from CSV
    ---
    tags:
      - Patients
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: CSV file containing patient data
    responses:
      200:
        description: Patients uploaded successfully
      400:
        description: Invalid or missing file
    """
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']
        if not file or file.filename == '':
            return jsonify({"error": "Empty filename"}), 400

        # Print for debugging (optional)
        print("Received file:", file.filename)

        # Read and parse CSV
        stream = io.StringIO(file.stream.read().decode("utf-8"), newline=None)
        reader = csv.DictReader(stream)

        required_fields = {'name'}
        added = 0
        skipped = 0

        for row in reader:
            print("Row:", row)  # Debug: See what the row looks like
            if not required_fields.issubset(row.keys()):
                skipped += 1
                continue

            name = row.get('name')
            if not name or not name.strip():
                skipped += 1
                continue

            gender = row.get('gender')
            birth_date = row.get('birth_date')
            contact_info = row.get('contact_info')

            # Parse birth_date safely
            birth_date_parsed = None
            if birth_date:
                try:
                    birth_date_parsed = datetime.strptime(birth_date, '%Y-%m-%d').date()
                except Exception as e:
                    print(f"Invalid birth_date: {birth_date} for row {row} - {e}")
                    birth_date_parsed = None

            patient = Patient(
                name=name,
                gender=gender,
                birth_date=birth_date_parsed,
                contact_info=contact_info
            )
            db.session.add(patient)
            added += 1

        db.session.commit()

        return jsonify({
            "message": f"{added} patients added successfully",
            "skipped": skipped
        }), 200

    except Exception as e:
        print("Bulk upload error:\n", traceback.format_exc())
        return jsonify({"error": "Failed to process file"}), 500
