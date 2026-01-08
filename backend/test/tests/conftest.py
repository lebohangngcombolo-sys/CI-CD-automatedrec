import pytest
from flask_jwt_extended import create_access_token
from unittest.mock import MagicMock
from app import create_app, db
from app.models import User

# -----------------------------
# App & DB fixtures
# -----------------------------
@pytest.fixture(scope="session")
def app():
    app = create_app("testing")
    with app.app_context():
        db.create_all()  # Create all tables in Postgres test DB
        yield app
        db.drop_all()  # Clean up after tests


@pytest.fixture(scope="function")
def client(app):
    """Return a test client for the app."""
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

    # JWT token must be created within app context
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
@pytest.fixture(scope="function", autouse=True)
def mock_openai(monkeypatch):
    """
    Mock OpenAI client for all tests to prevent actual API calls.
    """
    from app.services import cv_parser_service

    mock_client = MagicMock()
    # Replace OpenAI with mock in the service module
    monkeypatch.setattr(cv_parser_service, "OpenAI", lambda *args, **kwargs: mock_client)
    return mock_client
