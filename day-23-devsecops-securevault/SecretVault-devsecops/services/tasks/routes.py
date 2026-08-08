from datetime import datetime, timezone

from flask import Blueprint, jsonify, request

from services.auth.models import User
from services.tasks.models import Task
from shared.db import db
from shared.security import token_required


tasks_bp = Blueprint("tasks", __name__)
VALID_STATUSES = {"todo", "in_progress", "done"}
VALID_PRIORITIES = {"low", "medium", "high"}


@tasks_bp.route("/", methods=["GET"])
@token_required(User)
def get_tasks(current_user):
    status_filter = request.args.get("status")
    query = Task.query.filter_by(user_id=current_user.id)
    if status_filter and status_filter in VALID_STATUSES:
        query = query.filter_by(status=status_filter)
    tasks = query.order_by(Task.updated_at.desc()).all()
    return jsonify({"tasks": [task.to_dict() for task in tasks]}), 200


@tasks_bp.route("/stats", methods=["GET"])
@token_required(User)
def get_task_stats(current_user):
    total = Task.query.filter_by(user_id=current_user.id).count()
    todo = Task.query.filter_by(user_id=current_user.id, status="todo").count()
    in_progress = Task.query.filter_by(user_id=current_user.id, status="in_progress").count()
    done = Task.query.filter_by(user_id=current_user.id, status="done").count()
    high_priority = Task.query.filter_by(user_id=current_user.id, priority="high").count()
    return jsonify({"total": total, "todo": todo, "in_progress": in_progress, "done": done, "high_priority": high_priority}), 200


@tasks_bp.route("/<int:task_id>", methods=["GET"])
@token_required(User)
def get_task(current_user, task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"task": task.to_dict()}), 200


@tasks_bp.route("/", methods=["POST"])
@token_required(User)
def create_task(current_user):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    title = data.get("title", "").strip()
    if not title:
        return jsonify({"error": "Title is required"}), 400

    status = data.get("status", "todo")
    priority = data.get("priority", "medium")
    if status not in VALID_STATUSES:
        return jsonify({"error": f"Status must be one of {sorted(VALID_STATUSES)}"}), 400
    if priority not in VALID_PRIORITIES:
        return jsonify({"error": f"Priority must be one of {sorted(VALID_PRIORITIES)}"}), 400

    due_date = None
    if data.get("due_date"):
        try:
            due_date = datetime.fromisoformat(data["due_date"])
        except ValueError:
            return jsonify({"error": "Invalid due_date format. Use ISO 8601."}), 400

    task = Task(
        title=title,
        description=data.get("description", ""),
        status=status,
        priority=priority,
        due_date=due_date,
        user_id=current_user.id,
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({"message": "Task created", "task": task.to_dict()}), 201


@tasks_bp.route("/<int:task_id>", methods=["PUT"])
@token_required(User)
def update_task(current_user, task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    if "title" in data:
        task.title = data["title"].strip()
    if "description" in data:
        task.description = data["description"]
    if "status" in data:
        if data["status"] not in VALID_STATUSES:
            return jsonify({"error": f"Status must be one of {sorted(VALID_STATUSES)}"}), 400
        task.status = data["status"]
    if "priority" in data:
        if data["priority"] not in VALID_PRIORITIES:
            return jsonify({"error": f"Priority must be one of {sorted(VALID_PRIORITIES)}"}), 400
        task.priority = data["priority"]
    if "due_date" in data:
        if data["due_date"]:
            try:
                task.due_date = datetime.fromisoformat(data["due_date"])
            except ValueError:
                return jsonify({"error": "Invalid due_date format"}), 400
        else:
            task.due_date = None

    task.updated_at = datetime.now(timezone.utc)
    db.session.commit()
    return jsonify({"message": "Task updated", "task": task.to_dict()}), 200


@tasks_bp.route("/<int:task_id>", methods=["DELETE"])
@token_required(User)
def delete_task(current_user, task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"}), 200
