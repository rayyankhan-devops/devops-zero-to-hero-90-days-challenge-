from flask import Blueprint, jsonify, request

from services.notes.models import Note
from services.auth.models import User
from shared.db import db
from shared.security import token_required


notes_bp = Blueprint("notes", __name__)


@notes_bp.route("/", methods=["GET"])
@token_required(User)
def get_notes(current_user):
    notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.is_pinned.desc(), Note.updated_at.desc()).all()
    return jsonify({"notes": [note.to_dict() for note in notes]}), 200


@notes_bp.route("/<int:note_id>", methods=["GET"])
@token_required(User)
def get_note(current_user, note_id):
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first()
    if not note:
        return jsonify({"error": "Note not found"}), 404
    return jsonify({"note": note.to_dict()}), 200


@notes_bp.route("/", methods=["POST"])
@token_required(User)
def create_note(current_user):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    title = data.get("title", "").strip()
    content = data.get("content", "").strip()
    if not title:
        return jsonify({"error": "Title is required"}), 400
    if not content:
        return jsonify({"error": "Content is required"}), 400

    note = Note(
        title=title,
        content=content,
        is_pinned=bool(data.get("is_pinned", False)),
        color=data.get("color", "default"),
        user_id=current_user.id,
    )
    db.session.add(note)
    db.session.commit()
    return jsonify({"message": "Note created", "note": note.to_dict()}), 201


@notes_bp.route("/<int:note_id>", methods=["PUT"])
@token_required(User)
def update_note(current_user, note_id):
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first()
    if not note:
        return jsonify({"error": "Note not found"}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    if "title" in data:
        note.title = data["title"].strip()
    if "content" in data:
        note.content = data["content"].strip()
    if "is_pinned" in data:
        note.is_pinned = bool(data["is_pinned"])
    if "color" in data:
        note.color = data["color"]

    db.session.commit()
    return jsonify({"message": "Note updated", "note": note.to_dict()}), 200


@notes_bp.route("/<int:note_id>", methods=["DELETE"])
@token_required(User)
def delete_note(current_user, note_id):
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first()
    if not note:
        return jsonify({"error": "Note not found"}), 404

    db.session.delete(note)
    db.session.commit()
    return jsonify({"message": "Note deleted"}), 200
