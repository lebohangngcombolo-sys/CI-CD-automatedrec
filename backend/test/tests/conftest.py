import pytest
import os
import time
from flask_jwt_extended import create_access_token
from unittest.mock import MagicMock, patch
from psycopg2 import OperationalError
from app import create_app, db
from app.models import User

# -----------------------------
# App & DB fixtures
# -----------------------------
@pytest.fixture(scope="session")
def app():
    """Create app with database retry logic for CI/CD."""
    app = create_app("testing")
    
    # Set environment variables for testing
    os.environ['DATABASE_URL'] = os.environ.get('DATABASE_URL', 
        'postgresql://test_user:test_password@localhost:5432/recruitment_test_db')
    os.environ['REDIS_URL'] = os.environ.get('REDIS_URL', 
        'redis://localhost:6379/0')
    os.environ['FLASK_ENV'] = 'testing'
    
    # Retry database connection (important for CI/CD)
    max_retries = 10
    for attempt in range(max_retries):
        try:
            with app.app_context():
                db.create_all()  # Create all tables in Postgres test DB
                print(f"✓ Database connection successful (attempt {attempt + 1})")
                break
        except OperationalError as e:
            if attempt < max_retries - 1:
                print(f"⚠️ Database not ready, retrying... (attempt {attempt + 1}/{max_retries})")
                time.sleep(2)
            else:
                print(f"❌ Failed to connect to database after {max_retries} attempts")
                raise
    
    yield app
    
    # Clean up after tests
    with app.app_context():
        try:
            db.session.remove()
            db.drop_all()
            print("✓ Database cleanup completed")
        except Exception as e:
            print(f"⚠️ Error during cleanup: {e}")
            db.session.rollback()


@pytest.fixture(scope="function")
def client(app):
    """Return a test client for the app."""
    return app.test_client()


@pytest.fixture(scope="function", autouse=True)
def clean_db(app):
    """Ensure DB isolation per test."""
    with app.app_context():
        yield
        try:
            # Clean up all tables in reverse order to avoid foreign key constraints
            for table in reversed(db.metadata.sorted_tables):
                db.session.execute(table.delete())
            db.session.commit()
            db.session.remove()
        except Exception as e:
            db.session.rollback()
            print(f"⚠️ Error cleaning database: {e}")
            raise


# -----------------------------
# User fixtures
# -----------------------------
@pytest.fixture(scope="function")
def admin_user(app):
    """Create an admin user for testing."""
    with app.app_context():
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
    """Create an HR user for testing."""
    with app.app_context():
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
    
    # Configure mock responses for common OpenAI calls
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = '{"skills": ["Python", "Flask"], "experience": 3}'
    mock_client.chat.completions.create.return_value = mock_response
    
    # Replace OpenAI with mock in the service module
    monkeypatch.setattr(cv_parser_service, "OpenAI", lambda *args, **kwargs: mock_client)
    
    return mock_client


# -----------------------------
# Redis Mock Fixture
# -----------------------------
@pytest.fixture(scope="function", autouse=True)
def mock_redis(monkeypatch):
    """
    Mock Redis for testing to avoid connection issues.
    """
    mock_redis_client = MagicMock()
    mock_redis_client.ping.return_value = True
    mock_redis_client.get.return_value = None
    mock_redis_client.set.return_value = True
    mock_redis_client.delete.return_value = True
    
    # Mock Redis connection
    monkeypatch.setattr('app.extensions.cache', mock_redis_client)
    
    # Also mock flask_caching
    try:
        from app import cache
        monkeypatch.setattr(cache, 'cache', mock_redis_client)
    except ImportError:
        pass
    
    return mock_redis_client


# -----------------------------
# SSO Mock Fixture
# -----------------------------
@pytest.fixture(scope="function", autouse=True)
def disable_sso(monkeypatch):
    """
    Disable SSO for testing to avoid external HTTP calls.
    """
    # Mock SSO to always be disabled
    monkeypatch.setattr('app.config.SSO_ENABLED', False)
    monkeypatch.setattr('app.routes.sso_routes.SSO_ENABLED', False)
    
    # Mock metadata fetch to avoid HTTP calls
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '<?xml version="1.0"?>'
    
    monkeypatch.setattr('requests.get', lambda *args, **kwargs: mock_response)


# -----------------------------
# Test Configuration
# -----------------------------
def pytest_configure(config):
    """Pytest configuration hook."""
    # Set test markers
    config.addinivalue_line(
        "markers", "slow: mark test as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection."""
    # Skip tests that require external services if needed
    for item in items:
        if "external" in item.keywords:
            item.add_marker(pytest.mark.skip(reason="External service test"))