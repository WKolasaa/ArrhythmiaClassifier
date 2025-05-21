from app.extensions import db
from datetime import datetime

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    contact_info = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Patient {self.name}>'
