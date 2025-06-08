from app.extensions import db
from datetime import datetime
from sqlalchemy import JSON

class Heartbeat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    ecg_features = db.Column(JSON)  # Stores the 188-length ECG feature vector

    heartbeat_type = db.Column(db.String(5))  # Ground truth label
    predicted_type = db.Column(db.String(64))  # e.g., 'Normal', 'Arrhythmic'
    prediction_confidence = db.Column(db.Float)
    model_name = db.Column(db.String(100), nullable=False)

    patient = db.relationship('Patient', backref=db.backref('heartbeats', lazy=True))

    def __repr__(self):
        return f'<Heartbeat for Patient {self.patient_id}>'