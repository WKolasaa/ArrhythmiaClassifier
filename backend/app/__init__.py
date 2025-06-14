from flask import Flask
from app.extensions import db
from app.routes import auth, patient_routes, model
import os
import time
from sqlalchemy.exc import OperationalError
from flasgger import Swagger
from flask_cors import CORS
import sys


def create_app():
    sys.stdout.reconfigure(line_buffering=True)

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

    db.init_app(app)

    CORS(app, origins=["http://20.82.105.66:5173"])

    app.register_blueprint(auth.bp)
    app.register_blueprint(patient_routes.bp)
    app.register_blueprint(model.bp)
    app.register_blueprint(model.bpM)


    Swagger(app)

    with app.app_context():
        for i in range(10):
            try:
                db.create_all()
                print("Database connected.")
                break
            except OperationalError:
                print(f"Waiting for DB... ({i + 1}/10)")
                time.sleep(3)
        else:
            print("Database connection failed after 10 attempts.")

    return app
