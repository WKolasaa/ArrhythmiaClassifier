from app.extensions import db
from datetime import datetime

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    label = db.Column(db.String(50), nullable=False)
    model_used = db.Column(db.String(100), nullable=False)     
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)