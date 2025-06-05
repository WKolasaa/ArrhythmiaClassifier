from faker import Faker
from app.extensions import db
from app.models.patient import Patient
from app.models.heartbeat import Heartbeat
from datetime import datetime, timedelta
import random
from app import create_app

fake = Faker()

app = create_app()
app.app_context().push()  # Needed for DB access in script

def seed_patients(n=5):
    for _ in range(n):
        patient = Patient(
            name=fake.name(),
            gender=random.choice(['Male', 'Female', 'Other']),
            birth_date=fake.date_of_birth(),
            contact_info=fake.phone_number()
        )
        db.session.add(patient)
        db.session.flush()  # Get patient.id before commit

        # Add heartbeats
        for _ in range(100):
            heartbeat = Heartbeat(
                patient_id=patient.id,
                timestamp=datetime.utcnow() - timedelta(seconds=random.randint(0, 100000)),
                pre_RR=random.uniform(200, 400),
                post_RR=random.uniform(200, 400),
                p_peak=random.uniform(-0.2, 0.2),
                t_peak=random.uniform(-0.5, 0.5),
                r_peak=random.uniform(0.5, 1.5),
                s_peak=random.uniform(-0.5, 0.0),
                q_peak=random.uniform(-0.1, 0.1),
                qrs_interval=random.uniform(60, 120),
                pq_interval=random.uniform(120, 200),
                qt_interval=random.uniform(300, 450),
                st_interval=random.uniform(80, 120),
                qrs_morph0=random.uniform(-1, 1),
                qrs_morph1=random.uniform(-1, 1),
                qrs_morph2=random.uniform(-1, 1),
                qrs_morph3=random.uniform(-1, 1),
                qrs_morph4=random.uniform(-1, 1),
                heartbeat_type=random.choice(['N', 'V', 'A']),
                predicted_type=random.choice(['Normal', 'Arrhythmic']),
                prediction_confidence=round(random.uniform(0.7, 1.0), 2)
            )
            db.session.add(heartbeat)

    db.session.commit()
    print(f"Seeded {n} patients with heartbeat data.")

if __name__ == '__main__':
    seed_patients(n=10)
