"""
SecureVault - Authentication utilities (JWT-based)
"""

import jwt
import hashlib
import os
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify, current_app
from database import db, User


def hash_password(password: str) -> str:
    """Hash password using SHA-256 with a salt."""
    salt = os.environ.get("PASSWORD_SALT", "securevault-salt")
    return hashlib.sha256(f"{salt}{password}".encode()).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a plain password against its hash."""
    return hash_password(password) == password_hash


def generate_token(user_id: int) -> str:
    """Generate a JWT access token."""
    now = datetime.now(timezone.utc)
    expiration = now + timedelta(
        hours=current_app.config.get("JWT_EXPIRATION_HOURS", 24)
    )
    payload = {"user_id": user_id, "exp": expiration, "iat": now}
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")


def decode_token(token: str) -> dict:
    """Decode and validate a JWT token."""
    return jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])


def token_required(f):
    """Decorator to protect API routes with JWT authentication."""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"error": "Authentication token is missing"}), 401

        try:
            payload = decode_token(token)
            current_user = db.session.get(User, payload["user_id"])
            if not current_user or not current_user.is_active:
                return jsonify({"error": "Invalid or inactive user"}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(current_user, *args, **kwargs)

    return decorated
