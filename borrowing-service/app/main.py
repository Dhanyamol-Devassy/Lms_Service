from flask import Flask
from app.routes import bp
from prometheus_flask_exporter import PrometheusMetrics
from app.database import db
import time
import os

def create_app():
    app = Flask(__name__)

    # Load DB config from environment or use default
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "mysql+mysqlconnector://lms_user1:password@mysql/lms_borrowing"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Register extensions
    db.init_app(app)
    PrometheusMetrics(app)

    # Retry DB connection before creating tables
    with app.app_context():
        for i in range(10):
            try:
                db.create_all()
                print("Borrowing DB connected and initialized.")
                break
            except Exception as e:
                print(f"Attempt {i+1}: Waiting for DB... {e}")
                time.sleep(2)

    # Register routes
    app.register_blueprint(bp)

    return app

# Optional direct run for local dev
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5003)
