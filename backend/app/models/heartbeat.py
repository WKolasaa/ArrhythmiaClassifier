from app.extensions import db
from datetime import datetime
class Heartbeat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Features from CSV
    pre_RR = db.Column(db.Float)
    post_RR = db.Column(db.Float)
    p_peak = db.Column(db.Float)
    t_peak = db.Column(db.Float)
    r_peak = db.Column(db.Float)
    s_peak = db.Column(db.Float)
    q_peak = db.Column(db.Float)
    qrs_interval = db.Column(db.Float)
    pq_interval = db.Column(db.Float)
    qt_interval = db.Column(db.Float)
    st_interval = db.Column(db.Float)
    qrs_morph0 = db.Column(db.Float)
    qrs_morph1 = db.Column(db.Float)
    qrs_morph2 = db.Column(db.Float)
    qrs_morph3 = db.Column(db.Float)
    qrs_morph4 = db.Column(db.Float)

    # Label from dataset
    heartbeat_type = db.Column(db.String(5))  # Ground truth e.g., 'N', 'V', etc.

    # Model prediction (optional)
    predicted_type = db.Column(db.String(20))         # e.g., 'Normal', 'Arrhythmic'
    prediction_confidence = db.Column(db.Float)       # optional: if using probability scores

    patient = db.relationship('Patient', backref=db.backref('heartbeats', lazy=True))

    def __repr__(self):
        return f'<Heartbeat {self.heartbeat_type} for Patient {self.patient_id}>'
