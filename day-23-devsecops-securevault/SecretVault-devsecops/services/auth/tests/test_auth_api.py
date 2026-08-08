import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from services.auth.app import app as flask_app
from shared.db import db


@pytest.fixture
def app():
    flask_app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        SECRET_KEY="test-secret-key",
        JWT_EXPIRATION_HOURS=1,
    )
    with flask_app.app_context():
        db.drop_all()
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_headers(client):
    res = client.post("/api/auth/register", json={"username": "testuser", "email": "test@example.com", "password": "password123"})
    token = json.loads(res.data)["token"]
    return {"Authorization": f"Bearer {token}"}


def test_register_and_login(client):
    res = client.post("/api/auth/register", json={"username": "newuser", "email": "new@example.com", "password": "password123"})
    assert res.status_code == 201
    login = client.post("/api/auth/login", json={"identifier": "newuser", "password": "password123"})
    assert login.status_code == 200


def test_profile_roundtrip(client, auth_headers):
    res = client.get("/api/auth/profile", headers=auth_headers)
    assert res.status_code == 200
    update = client.put("/api/auth/profile", headers=auth_headers, json={"username": "updateduser"})
    assert update.status_code == 200
