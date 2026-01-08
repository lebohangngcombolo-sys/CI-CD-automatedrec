import pytest
from app import db
from app.models import User, Requisition, Candidate, Application
from flask_jwt_extended import create_access_token
from datetime import timedelta

# ---------------------- HAPPY PATH TESTS ----------------------
def test_list_users(client, admin_user):
    headers = {'Authorization': f'Bearer {admin_user.token}'}
    response = client.get('/users', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

def test_create_job_success(client, admin_user):
    headers = {'Authorization': f'Bearer {admin_user.token}'}
    payload = {
        "title": "Test Job",
        "description": "Job description",
        "vacancy": 2,
        "category": "Engineering",
        "weightings": {"cv": 60, "assessment": 40}
    }
    response = client.post('/jobs', headers=headers, json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["job"]["title"] == "Test Job"

def test_get_job_success(client, admin_user):
    job = Requisition(title="Get Job", description="desc", vacancy=1, category="Cat", weightings={"cv":50,"assessment":50})
    db.session.add(job)
    db.session.commit()
    headers = {'Authorization': f'Bearer {admin_user.token}'}
    response = client.get(f'/jobs/{job.id}', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Get Job"

def test_list_candidates(client, admin_user):
    candidate = Candidate(full_name="Alice")
    db.session.add(candidate)
    db.session.commit()
    headers = {'Authorization': f'Bearer {admin_user.token}'}
    response = client.get('/candidates', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert any(c["full_name"]=="Alice" for c in data)

# ---------------------- EDGE CASES ----------------------
def test_get_nonexistent_job(client, admin_user):
    headers = {'Authorization': f'Bearer {admin_user.token}'}
    response = client.get('/jobs/9999', headers=headers)
    assert response.status_code == 404

def test_delete_nonexistent_user(client, admin_user):
    headers = {'Authorization': f'Bearer {admin_user.token}'}
    response = client.delete('/users/9999', headers=headers)
    assert response.status_code == 404

def test_get_nonexistent_application(client, admin_user):
    headers = {'Authorization': f'Bearer {admin_user.token}'}
    response = client.get('/applications/9999', headers=headers)
    assert response.status_code == 404

def test_access_without_token(client):
    response = client.get('/jobs')
    assert response.status_code == 401

def test_hr_cannot_delete_job(client, hr_user):
    headers = {'Authorization': f'Bearer {hr_user.token}'}
    response = client.delete('/jobs/1', headers=headers)
    assert response.status_code == 403

def test_jobs_pagination(client, admin_user):
    headers = {'Authorization': f'Bearer {admin_user.token}'}
    for i in range(15):
        db.session.add(Requisition(title=f"Job {i}", description="desc", vacancy=1, category="Cat", weightings={"cv":50,"assessment":50}))
    db.session.commit()
    response = client.get('/jobs?per_page=5&page=2', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['jobs']) <= 5

def test_candidates_filter_by_skill(client, admin_user):
    headers = {'Authorization': f'Bearer {admin_user.token}'}
    db.session.add(Candidate(full_name="Alice", skills=["Python"]))
    db.session.add(Candidate(full_name="Bob", skills=["Java"]))
    db.session.commit()
    response = client.get('/candidates', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert any("Python" in c.get("skills",[]) for c in data)

def test_create_job_invalid_payload(client, admin_user):
    headers = {'Authorization': f'Bearer {admin_user.token}'}
    payload = {"title": "", "vacancy": -1}  # missing required fields
    response = client.post('/jobs', headers=headers, json=payload)
    assert response.status_code == 400

def test_empty_candidates_list(client, admin_user):
    Candidate.query.delete()
    db.session.commit()
    headers = {'Authorization': f'Bearer {admin_user.token}'}
    response = client.get('/candidates', headers=headers)
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 0

def test_empty_jobs_list(client, admin_user):
    Requisition.query.delete()
    db.session.commit()
    headers = {'Authorization': f'Bearer {admin_user.token}'}
    response = client.get('/jobs', headers=headers)
    data = response.get_json()
    assert isinstance(data['jobs'], list)
    assert len(data['jobs']) == 0

def test_invalid_token(client):
    headers = {'Authorization': 'Bearer invalidtoken123'}
    response = client.get('/jobs', headers=headers)
    assert response.status_code == 422

def test_expired_token(client):
    user = User(email="temp@test.com", role="admin")
    db.session.add(user)
    db.session.commit()
    token = create_access_token(identity=user.id, expires_delta=timedelta(seconds=-1))
    headers = {'Authorization': f'Bearer {token}'}
    response = client.get('/jobs', headers=headers)
    assert response.status_code == 401
