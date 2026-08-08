"""
SecureVault - Unit Tests
Run with: pytest tests/ -v
"""

import pytest
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app as flask_app
from database import db, User, Note, Task
from auth_utils import hash_password, verify_password, generate_token


# ─── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture
def app():
    flask_app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        SECRET_KEY="test-secret-key",
        JWT_EXPIRATION_HOURS=1,
    )
    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_headers(client):
    """Register a test user and return auth headers."""
    res = client.post(
        "/api/auth/register",
        json={"username": "testuser", "email": "test@example.com", "password": "password123"},
    )
    token = json.loads(res.data)["token"]
    return {"Authorization": f"Bearer {token}"}


# ─── Auth Tests ────────────────────────────────────────────────────────────────

class TestAuthUtils:
    def test_hash_password_deterministic(self):
        h1 = hash_password("mypassword")
        h2 = hash_password("mypassword")
        assert h1 == h2

    def test_hash_different_passwords(self):
        assert hash_password("password1") != hash_password("password2")

    def test_verify_password_correct(self):
        hashed = hash_password("correct")
        assert verify_password("correct", hashed) is True

    def test_verify_password_wrong(self):
        hashed = hash_password("correct")
        assert verify_password("wrong", hashed) is False


class TestAuthEndpoints:
    def test_register_success(self, client):
        res = client.post(
            "/api/auth/register",
            json={"username": "newuser", "email": "new@example.com", "password": "pass123"},
        )
        assert res.status_code == 201
        data = json.loads(res.data)
        assert "token" in data
        assert data["user"]["username"] == "newuser"

    def test_register_duplicate_username(self, client, auth_headers):
        res = client.post(
            "/api/auth/register",
            json={"username": "testuser", "email": "other@example.com", "password": "pass123"},
        )
        assert res.status_code == 409

    def test_register_short_password(self, client):
        res = client.post(
            "/api/auth/register",
            json={"username": "user2", "email": "u2@example.com", "password": "abc"},
        )
        assert res.status_code == 400

    def test_register_invalid_email(self, client):
        res = client.post(
            "/api/auth/register",
            json={"username": "user3", "email": "notanemail", "password": "pass123"},
        )
        assert res.status_code == 400

    def test_login_success(self, client, auth_headers):
        res = client.post(
            "/api/auth/login",
            json={"identifier": "testuser", "password": "password123"},
        )
        assert res.status_code == 200
        data = json.loads(res.data)
        assert "token" in data

    def test_login_by_email(self, client, auth_headers):
        res = client.post(
            "/api/auth/login",
            json={"identifier": "test@example.com", "password": "password123"},
        )
        assert res.status_code == 200

    def test_login_wrong_password(self, client, auth_headers):
        res = client.post(
            "/api/auth/login",
            json={"identifier": "testuser", "password": "wrongpass"},
        )
        assert res.status_code == 401

    def test_get_profile_authenticated(self, client, auth_headers):
        res = client.get("/api/auth/profile", headers=auth_headers)
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data["user"]["username"] == "testuser"

    def test_get_profile_unauthenticated(self, client):
        res = client.get("/api/auth/profile")
        assert res.status_code == 401


# ─── Notes Tests ──────────────────────────────────────────────────────────────

class TestNotesEndpoints:
    def test_create_note(self, client, auth_headers):
        res = client.post(
            "/api/notes/",
            json={"title": "My First Note", "content": "This is secure content."},
            headers=auth_headers,
        )
        assert res.status_code == 201
        data = json.loads(res.data)
        assert data["note"]["title"] == "My First Note"

    def test_create_note_missing_title(self, client, auth_headers):
        res = client.post(
            "/api/notes/",
            json={"content": "No title here"},
            headers=auth_headers,
        )
        assert res.status_code == 400

    def test_get_notes(self, client, auth_headers):
        # Create two notes
        client.post("/api/notes/", json={"title": "Note 1", "content": "Content 1"}, headers=auth_headers)
        client.post("/api/notes/", json={"title": "Note 2", "content": "Content 2"}, headers=auth_headers)

        res = client.get("/api/notes/", headers=auth_headers)
        assert res.status_code == 200
        data = json.loads(res.data)
        assert len(data["notes"]) == 2

    def test_update_note(self, client, auth_headers):
        create_res = client.post(
            "/api/notes/",
            json={"title": "Original", "content": "Original content"},
            headers=auth_headers,
        )
        note_id = json.loads(create_res.data)["note"]["id"]

        res = client.put(
            f"/api/notes/{note_id}",
            json={"title": "Updated Title"},
            headers=auth_headers,
        )
        assert res.status_code == 200
        assert json.loads(res.data)["note"]["title"] == "Updated Title"

    def test_delete_note(self, client, auth_headers):
        create_res = client.post(
            "/api/notes/",
            json={"title": "Delete me", "content": "Temporary"},
            headers=auth_headers,
        )
        note_id = json.loads(create_res.data)["note"]["id"]

        res = client.delete(f"/api/notes/{note_id}", headers=auth_headers)
        assert res.status_code == 200

        get_res = client.get(f"/api/notes/{note_id}", headers=auth_headers)
        assert get_res.status_code == 404

    def test_cannot_access_other_users_note(self, client):
        # Create user1
        res1 = client.post(
            "/api/auth/register",
            json={"username": "user1", "email": "u1@test.com", "password": "pass123"},
        )
        headers1 = {"Authorization": f"Bearer {json.loads(res1.data)['token']}"}
        note_res = client.post("/api/notes/", json={"title": "Private", "content": "Secret"}, headers=headers1)
        note_id = json.loads(note_res.data)["note"]["id"]

        # Create user2
        res2 = client.post(
            "/api/auth/register",
            json={"username": "user2", "email": "u2@test.com", "password": "pass123"},
        )
        headers2 = {"Authorization": f"Bearer {json.loads(res2.data)['token']}"}

        # User2 tries to access user1's note
        res = client.get(f"/api/notes/{note_id}", headers=headers2)
        assert res.status_code == 404


# ─── Tasks Tests ──────────────────────────────────────────────────────────────

class TestTasksEndpoints:
    def test_create_task(self, client, auth_headers):
        res = client.post(
            "/api/tasks/",
            json={"title": "Deploy to production", "priority": "high"},
            headers=auth_headers,
        )
        assert res.status_code == 201
        data = json.loads(res.data)
        assert data["task"]["priority"] == "high"
        assert data["task"]["status"] == "todo"

    def test_create_task_invalid_priority(self, client, auth_headers):
        res = client.post(
            "/api/tasks/",
            json={"title": "Bad task", "priority": "critical"},
            headers=auth_headers,
        )
        assert res.status_code == 400

    def test_get_task_stats(self, client, auth_headers):
        client.post("/api/tasks/", json={"title": "T1", "status": "todo"}, headers=auth_headers)
        client.post("/api/tasks/", json={"title": "T2", "status": "done"}, headers=auth_headers)

        res = client.get("/api/tasks/stats", headers=auth_headers)
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data["total"] == 2
        assert data["done"] == 1

    def test_update_task_status(self, client, auth_headers):
        create_res = client.post(
            "/api/tasks/",
            json={"title": "Work in progress"},
            headers=auth_headers,
        )
        task_id = json.loads(create_res.data)["task"]["id"]

        res = client.put(
            f"/api/tasks/{task_id}",
            json={"status": "in_progress"},
            headers=auth_headers,
        )
        assert res.status_code == 200
        assert json.loads(res.data)["task"]["status"] == "in_progress"

    def test_delete_task(self, client, auth_headers):
        create_res = client.post("/api/tasks/", json={"title": "Temp task"}, headers=auth_headers)
        task_id = json.loads(create_res.data)["task"]["id"]

        res = client.delete(f"/api/tasks/{task_id}", headers=auth_headers)
        assert res.status_code == 200


# ─── Health Check ──────────────────────────────────────────────────────────────

class TestHealthCheck:
    def test_health_endpoint(self, client):
        res = client.get("/api/health")
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data["status"] == "healthy"
