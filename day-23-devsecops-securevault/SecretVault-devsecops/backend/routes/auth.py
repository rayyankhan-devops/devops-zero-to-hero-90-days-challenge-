"""
SecureVault - Authentication Routes
Handles register, login, logout, and profile operations.
"""

from flask import Blueprint, request, jsonify
from database import db, User
from auth_utils import hash_password, verify_password, generate_token, token_required

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    """Register a new user account."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    username = data.get("username", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    # Validation
    if not username or not email or not password:
        return jsonify({"error": "Username, email, and password are required"}), 400

    if len(username) < 3:
        return jsonify({"error": "Username must be at least 3 characters"}), 400

    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    if "@" not in email:
        return jsonify({"error": "Invalid email address"}), 400

    # Check uniqueness
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already taken"}), 409

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409

    # Create user
    user = User(
        username=username,
        email=email,
        password_hash=hash_password(password),
    )
    db.session.add(user)
    db.session.commit()

    token = generate_token(user.id)
    return jsonify({"message": "Account created successfully", "token": token, "user": user.to_dict()}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """Authenticate a user and return a JWT token."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    identifier = data.get("identifier", "").strip()  # username or email
    password = data.get("password", "")

    if not identifier or not password:
        return jsonify({"error": "Identifier and password are required"}), 400

    # Find user by username or email
    user = User.query.filter(
        (User.username == identifier) | (User.email == identifier.lower())
    ).first()

    if not user or not verify_password(password, user.password_hash):
        return jsonify({"error": "Invalid credentials"}), 401

    if not user.is_active:
        return jsonify({"error": "Account is disabled"}), 403

    token = generate_token(user.id)
    return jsonify({"message": "Login successful", "token": token, "user": user.to_dict()}), 200


@auth_bp.route("/profile", methods=["GET"])
@token_required
def get_profile(current_user):
    """Get the authenticated user's profile."""
    return jsonify({"user": current_user.to_dict()}), 200


@auth_bp.route("/profile", methods=["PUT"])
@token_required
def update_profile(current_user):
    """Update username or email."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    if "username" in data:
        new_username = data["username"].strip()
        if len(new_username) < 3:
            return jsonify({"error": "Username must be at least 3 characters"}), 400
        existing = User.query.filter_by(username=new_username).first()
        if existing and existing.id != current_user.id:
            return jsonify({"error": "Username already taken"}), 409
        current_user.username = new_username

    if "email" in data:
        new_email = data["email"].strip().lower()
        if "@" not in new_email:
            return jsonify({"error": "Invalid email address"}), 400
        existing = User.query.filter_by(email=new_email).first()
        if existing and existing.id != current_user.id:
            return jsonify({"error": "Email already registered"}), 409
        current_user.email = new_email

    db.session.commit()
    return jsonify({"message": "Profile updated", "user": current_user.to_dict()}), 200
