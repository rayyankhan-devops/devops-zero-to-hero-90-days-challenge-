from flask import Flask
from flask_cors import CORS

from services.auth.models import User
from services.notes.routes import notes_bp
from shared.config import Settings
from shared.db import db
from shared.health import health_response


settings = Settings("notes-service")
app = Flask(__name__)
app.config.update(settings.flask_config())
CORS(app, resources={r"/api/*": {"origins": settings.cors_origins}})
db.init_app(app)
app.register_blueprint(notes_bp, url_prefix="/api/notes")


@app.route("/api/health")
def health_check():
    return health_response("notes-service")


with app.app_context():
    db.create_all()
