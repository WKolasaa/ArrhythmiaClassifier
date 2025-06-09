from app.models.heartbeat import Heartbeat
from app.models.retrainedmodel import TrainedModel
from app.ml.model import build_model, CLASS_MAP
from app.ml.labels import label_to_int
from app.extensions import db
from datetime import datetime
import os
import numpy as np
import tensorflow as tf

MODEL_FOLDER = os.path.join(os.getcwd(), "model")  
EXPECTED_FEATURE_LENGTH = 187
VALID_LABELS = set(CLASS_MAP.keys())
MAJOR_VERSION = 1 # Increment this for major changes

def run_retraining(app, user_id):
    with app.app_context():
        heartbeats = Heartbeat.query.filter(Heartbeat.heartbeat_type.isnot(None)).all()
        print(f"Loaded {len(heartbeats)} heartbeats from DB")

        EXPECTED_FEATURE_LENGTH = 187
        VALID_LABELS = set(CLASS_MAP.keys())

        valid_heartbeats = []
        skipped = []

        for hb in heartbeats:
            reasons = []

            if not isinstance(hb.ecg_features, list):
                reasons.append("features not list")
                skipped.append((hb.id, reasons))
                continue

            if len(hb.ecg_features) < EXPECTED_FEATURE_LENGTH:
                reasons.append(f"too short: {len(hb.ecg_features)}")
            elif len(hb.ecg_features) > EXPECTED_FEATURE_LENGTH + 2:
                reasons.append(f"too long: {len(hb.ecg_features)}")

            try:
                label_val = hb.ecg_features[EXPECTED_FEATURE_LENGTH] if len(hb.ecg_features) > EXPECTED_FEATURE_LENGTH else hb.heartbeat_type
                label = str(int(label_val))
                if label not in VALID_LABELS:
                    reasons.append(f"invalid label: {label}")
            except Exception as e:
                reasons.append(f"label error: {e}")

            if reasons:
                skipped.append((hb.id, reasons))
                continue

            features = hb.ecg_features[:EXPECTED_FEATURE_LENGTH]
            valid_heartbeats.append((features, label))

        print(f"Total heartbeats: {len(heartbeats)}")
        print(f"Valid heartbeats: {len(valid_heartbeats)}")
        print(f"Skipped: {len(skipped)}")
        print(f"Sample issues: {skipped[:5]}")

        if not valid_heartbeats:
            raise ValueError("No valid heartbeats to train on.")  

        X = np.stack([f for f, _ in valid_heartbeats]).reshape(-1, EXPECTED_FEATURE_LENGTH, 1)
        y = np.array([label_to_int(l) for _, l in valid_heartbeats])

        model = build_model(input_shape=(EXPECTED_FEATURE_LENGTH, 1), num_classes=len(CLASS_MAP))
        model.fit(X, y, epochs=10, batch_size=64, validation_split=0.2)

        os.makedirs(MODEL_FOLDER, exist_ok=True)
        last = TrainedModel.query.order_by(TrainedModel.id.desc()).first()
        next_minor = int(last.version.split('.')[-1]) + 1 if last else 1
        version = f"1.{next_minor}"

        filename = f"model_cnn_lstm_v{version.replace('.', '_')}.h5"
        model_path = os.path.join(MODEL_FOLDER, filename)
        model.save(model_path)

        new_entry = TrainedModel(
            version=version,
            file_path=model_path,
            user_id=user_id
        )
        db.session.add(new_entry)
        db.session.commit()

        print(f"Model version {version} saved to {model_path}")
        return version