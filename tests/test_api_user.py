from fastapi.testclient import TestClient
import uuid
from server.fast_api_server import app

def test_create_user():
    email = f"pytest_{uuid.uuid4().hex}@example.com"
    with TestClient(app) as client:
        response = client.post("/users/", json={
            "username": "pytest_user",
            "email": email,
            "password": "TestPassword123!"
        })

        assert response.status_code == 200
        assert response.json()["username"] == "pytest_user"
        assert response.json()["email"] == email
        assert isinstance(response.json(), dict)
        assert "password" not in response.json()
        assert "password_hash" not in response.json()


def test_login_success():
    with TestClient(app) as client:
        response = client.post("/users/login", json={
            "email": "pytest_user@example.com",
            "password": "TestPassword123!"
        })

        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"

def test_login_wrong_password():
    with TestClient(app) as client:
        response = client.post("/users/login", json={
            "email": "pytest_user@example.com",
            "password": "WrongPassword123!"
        })

        assert response.status_code == 401

