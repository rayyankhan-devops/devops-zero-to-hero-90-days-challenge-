"""
SecureVault - Main Flask Application
A secure notes/task management app built for DevSecOps demonstration.
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from database import db, init_db
from routes.auth import auth_bp
from routes.notes import notes_bp
from routes.tasks import tasks_bp

app = Flask(__name__, static_folder="../frontend", static_url_path="")

# Configuration
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///securevault.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_EXPIRATION_HOURS"] = 24

# Extensions
CORS(app, resources={r"/api/*": {"origins": "*"}})
db.init_app(app)

# Blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(notes_bp, url_prefix="/api/notes")
app.register_blueprint(tasks_bp, url_prefix="/api/tasks")


@app.route("/api/health")
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify({"status": "healthy", "service": "SecureVault API", "version": "1.0.0"})


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    """Serve the frontend SPA."""
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(debug=True, host="0.0.0.0", port=5001)
