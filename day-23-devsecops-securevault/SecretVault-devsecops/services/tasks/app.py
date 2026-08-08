from flask import Flask
from flask_cors import CORS

from services.auth.models import User
from services.tasks.routes import tasks_bp
from shared.config import Settings
from shared.db import db
from shared.health import health_response


settings = Settings("tasks-service")
app = Flask(__name__)
app.config.update(settings.flask_config())
CORS(app, resources={r"/api/*": {"origins": settings.cors_origins}})
db.init_app(app)
app.register_blueprint(tasks_bp, url_prefix="/api/tasks")


@app.route("/api/health")
def health_check():
    return health_response("tasks-service")


with app.app_context():
    db.create_all()
