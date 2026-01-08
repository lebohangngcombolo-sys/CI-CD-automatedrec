import pytest
from datetime import timedelta
from flask_jwt_extended import create_access_token

from app import db
from app.models import User, Requisition, Candidate


# ---------------------- HAPPY PATH TESTS ----------------------

def test_list_users(client, admin_user):
    headers = {"Authorization": f"Bearer {admin_user.token}"}
    response = client.get("/users", headers=headers)

    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_create_job_success(client, admin_user):
    headers = {"Authorization": f"Bearer {admin_user.token}"}
    payload = {
        "title": "Test Job",
        "description": "Job description",
        "vacancy": 2,
        "category": "Engineering",
        "weightings": {"cv": 60, "assessment": 40},
    }

    response = client.post("/jobs", headers=headers, json=payload)

    assert response.status_code == 201
    data = response.get_json()
    assert data["job"]["title"] == payload["title"]


def test_get_job_success(client, admin_user):
    job = Requisition(
        title="Get Job",
        description="desc",
        vacancy=1,
        category="Cat",
        weightings={"cv": 50, "assessment": 50},
    )
    db.session.add(job)
    db.session.commit()

    headers = {"Authorization": f"Bearer {admin_user.token}"}
    response = client.get(f"/jobs/{job.id}", headers=headers)

    assert response.status_code == 200
    assert response.get_json()["title"] == job.title


def test_list_candidates(client, admin_user):
    candidate = Candidate(full_name="Alice")
    db.session.add(candidate)
    db.session.commit()

    headers = {"Authorization": f"Bearer {admin_user.token}"}
    response = client.get("/candidates", headers=headers)

    assert response.status_code == 200
    assert any(c["full_name"] == "Alice" for c in response.get_json())


# ---------------------- EDGE CASES ----------------------

def test_get_nonexistent_job(client, admin_user):
    headers = {"Authorization": f"Bearer {admin_user.token}"}
    response = client.get("/jobs/999999", headers=headers)

    assert response.status_code == 404


def test_delete_nonexistent_user(client, admin_user):
    headers = {"Authorization": f"Bearer {admin_user.token}"}
    response = client.delete("/users/999999", headers=headers)

    assert response.status_code == 404


def test_access_without_token(client):
    response = client.get("/jobs")
    assert response.status_code == 401


def test_hr_cannot_delete_job(client, hr_user):
    job = Requisition(
        title="Protected Job",
        description="desc",
        vacancy=1,
        category="Cat",
        weightings={"cv": 50, "assessment": 50},
    )
    db.session.add(job)
    db.session.commit()

    headers = {"Authorization": f"Bearer {hr_user.token}"}
    response = client.delete(f"/jobs/{job.id}", headers=headers)

    assert response.status_code == 403


def test_jobs_pagination(client, admin_user):
    for i in range(15):
        db.session.add(
            Requisition(
                title=f"Job {i}",
                description="desc",
                vacancy=1,
                category="Cat",
                weightings={"cv": 50, "assessment": 50},
            )
        )
    db.session.commit()

    headers = {"Authorization": f"Bearer {admin_user.token}"}
    response = client.get("/jobs?per_page=5&page=2", headers=headers)

    assert response.status_code == 200
    assert len(response.get_json()["jobs"]) <= 5


def test_candidates_filter_by_skill(client, admin_user):
    db.session.add(Candidate(full_name="Alice", skills=["Python"]))
    db.session.add(Candidate(full_name="Bob", skills=["Java"]))
    db.session.commit()

    headers = {"Authorization": f"Bearer {admin_user.token}"}
    response = client.get("/candidates", headers=headers)

    assert response.status_code == 200
    assert any("Python" in c.get("skills", []) for c in response.get_json())


def test_create_job_invalid_payload(client, admin_user):
    headers = {"Authorization": f"Bearer {admin_user.token}"}
    payload = {"title": "", "vacancy": -1}

    response = client.post("/jobs", headers=headers, json=payload)

    assert response.status_code == 400


def test_invalid_token(client):
    headers = {"Authorization": "Bearer invalidtoken123"}
    response = client.get("/jobs", headers=headers)

    assert response.status_code == 422


def test_expired_token(app, client):
    user = User(email="temp@test.com", role="admin")
    db.session.add(user)
    db.session.commit()

    with app.app_context():
        token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(seconds=-1),
        )

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/jobs", headers=headers)

    assert response.status_code == 401
