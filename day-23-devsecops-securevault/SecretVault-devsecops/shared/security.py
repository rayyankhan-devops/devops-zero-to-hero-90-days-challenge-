import hashlib
import os
from datetime import datetime, timedelta, timezone

import jwt
from flask import current_app, jsonify, request
from functools import wraps

from shared.db import db


def hash_password(password: str) -> str:
    salt = os.environ.get("PASSWORD_SALT", "securevault-salt")
    return hashlib.sha256(f"{salt}{password}".encode()).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    return hash_password(password) == password_hash


def generate_token(user_id: int, extra_claims: dict | None = None) -> str:
    now = datetime.now(timezone.utc)
    expiration = now + timedelta(hours=current_app.config.get("JWT_EXPIRATION_HOURS", 24))
    payload = {"user_id": user_id, "exp": expiration, "iat": now}
    if extra_claims:
        payload.update(extra_claims)
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")


def decode_token(token: str) -> dict:
    return jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])


def require_bearer_token():
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header.split(" ", 1)[1]
    return None


def token_required(user_model):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = require_bearer_token()
            if not token:
                return jsonify({"error": "Authentication token is missing"}), 401

            try:
                payload = decode_token(token)
                current_user = db.session.get(user_model, payload["user_id"])
                if not current_user or not current_user.is_active:
                    return jsonify({"error": "Invalid or inactive user"}), 401
            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token has expired"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"error": "Invalid token"}), 401

            return f(current_user, *args, **kwargs)

        return decorated

    return decorator
