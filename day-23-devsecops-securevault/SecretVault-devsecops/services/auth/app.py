from flask import Flask
from flask_cors import CORS

from services.auth.models import User
from services.auth.routes import auth_bp
from shared.config import Settings
from shared.db import db
from shared.health import health_response


settings = Settings("auth-service")
app = Flask(__name__)
app.config.update(settings.flask_config())
CORS(app, resources={r"/api/*": {"origins": settings.cors_origins}})
db.init_app(app)
app.register_blueprint(auth_bp, url_prefix="/api/auth")


@app.route("/api/health")
def health_check():
    return health_response("auth-service")


@app.cli.command("init-db")
def init_db_command():
    with app.app_context():
        db.create_all()
        print("Auth database initialized")


with app.app_context():
    db.create_all()
