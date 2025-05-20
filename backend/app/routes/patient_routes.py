from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.patient import Patient
from datetime import datetime

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
    """
        List all patients
        ---
        tags:
          - Patients
        responses:
          200:
            description: A list of patients
            schema:
              type: array
              items:
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
        500:
          description: Server error
    """
    try:
        patients = Patient.query.all()
        result = []
        for p in patients:
            result.append({
                'id': p.id,
                'name': p.name,
                'gender': p.gender,
                'birth_date': p.birth_date.strftime('%Y-%m-%d') if p.birth_date else None,
                'contact_info': p.contact_info,
                'created_at': p.created_at.isoformat()
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
