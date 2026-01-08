import pytest
from flask_jwt_extended import create_access_token
from unittest.mock import MagicMock
import sys

from app import create_app, db
from app.models import User

# -----------------------------
# App & DB fixtures
# -----------------------------
@pytest.fixture(scope="session")
def app():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()


@pytest.fixture(scope="function", autouse=True)
def clean_db(app):
    """Ensure DB isolation per test."""
    yield
    db.session.rollback()
    for table in reversed(db.metadata.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()

# -----------------------------
# User fixtures
# -----------------------------
@pytest.fixture(scope="function")
def admin_user(app):
    admin = User(
        email="admin@test.com",
        role="admin",
        is_verified=True,
    )
    db.session.add(admin)
    db.session.commit()

    # JWT must be created within app context
    admin.token = create_access_token(identity=admin.id)
    return admin


@pytest.fixture(scope="function")
def hr_user(app):
    hr = User(
        email="hr@test.com",
        role="hr",
        is_verified=True,
    )
    db.session.add(hr)
    db.session.commit()

    hr.token = create_access_token(identity=hr.id)
    return hr

# -----------------------------
# OpenAI Mock Fixture (Autouse)
# -----------------------------
@pytest.fixture(scope="session", autouse=True)
def mock_openai(monkeypatch):
    """
    Globally mock OpenAI client for all tests to prevent API calls.
    """
    mock_client = MagicMock()
    monkeypatch.setattr("app.services.cv_parser_service.OpenAI", lambda *a, **kw: mock_client)
    return mock_client

