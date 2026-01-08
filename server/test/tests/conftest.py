import pytest
from app import db, create_app
from app.models import User
from flask_jwt_extended import create_access_token

@pytest.fixture(scope='module')
def app():
    app = create_app('testing')  # Make sure you have a testing config
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def admin_user(app):
    admin = User(email='admin@test.com', role='admin', is_verified=True)
    db.session.add(admin)
    db.session.commit()
    admin.token = create_access_token(identity=admin.id)
    return admin

@pytest.fixture
def hr_user(app):
    hr = User(email='hr@test.com', role='hr', is_verified=True)
    db.session.add(hr)
    db.session.commit()
    hr.token = create_access_token(identity=hr.id)
    return hr
