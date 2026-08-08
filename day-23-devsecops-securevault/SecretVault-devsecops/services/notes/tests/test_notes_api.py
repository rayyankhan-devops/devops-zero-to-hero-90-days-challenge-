import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from services.notes.app import app as flask_app
from services.auth.models import User
from shared.db import db
from shared.security import generate_token


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
    with flask_app.app_context():
        user = User(username="testuser", email="test@example.com", password_hash="hash")
        db.session.add(user)
        db.session.commit()
        token = generate_token(user.id)
    return {"Authorization": f"Bearer {token}"}


def test_create_and_list_notes(client, auth_headers):
    res = client.post("/api/notes/", headers=auth_headers, json={"title": "Note 1", "content": "Content"})
    assert res.status_code == 201
    listing = client.get("/api/notes/", headers=auth_headers)
    assert listing.status_code == 200
    assert len(json.loads(listing.data)["notes"]) == 1
