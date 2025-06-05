from app.extensions import db
from datetime import datetime

class ModelPerformance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(100), nullable=False)
    accuracy = db.Column(db.Float, nullable=True)
    confusion_matrix = db.Column(db.JSON, nullable=True)  # Stored as a nested list
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ModelPerformance {self.model_name} - {self.accuracy}>"
