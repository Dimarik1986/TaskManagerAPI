from fastapi.testclient import TestClient
from server.fast_api_server import app

import uuid

def get_token(client)-> str:
    response = client.post("/users/login", json={
        "email": "pytest_user@example.com",
        "password": "TestPassword123!"
    })
    assert response.status_code == 200
    return response.json()["access_token"]

def test_get_tasks():
    with TestClient(app) as client:
        token = get_token(client)
        response = client.get(
            "/tasks",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)

def test_create_task():
    with TestClient(app) as client:
        token = get_token(client)

        response = client.post(
            "/tasks",
            json={"title": "Test Task"},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        assert response.json()["title"] == "Test Task"
        assert isinstance(response.json(), dict)

def test_get_task():
    with TestClient(app) as client:
        token = get_token(client)
        headers = {"Authorization": f"Bearer {token}"}

        response = client.post(
            "/tasks",
            json={"title": "Test Task"},
            headers=headers
        )
        assert response.status_code == 200

        task_id = response.json()["id"]

        response = client.get(
            f"/tasks/{task_id}",
            headers=headers
        )
        assert response.status_code == 200
        assert response.json()["title"] == "Test Task"

def test_get_task_not_found():
    with TestClient(app) as client:
        token = get_token(client)
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get("/tasks/9999", headers=headers)

        assert response.status_code == 404

def test_delete_task():
    with TestClient(app) as client:
        token = get_token(client)
        headers = {"Authorization": f"Bearer {token}"}

        response = client.post(
            "/tasks",
            json={"title": "Test Task"},
            headers=headers
        )
        assert response.status_code == 200

        task_id = response.json()["id"]

        response = client.delete(
            f"/tasks/{task_id}",
            headers=headers
        )
        assert response.status_code == 204

        response = client.get(
            f"/tasks/{task_id}",
            headers=headers
        )
        assert response.status_code == 404


def test_patch_empty():
    with TestClient(app) as client:
        token = get_token(client)
        headers = {"Authorization": f"Bearer {token}"}

        response = client.post(
            "/tasks",
            json={"title": "Test Task"},
            headers=headers
        )
        assert response.status_code == 200

        task_id = response.json()["id"]

        response = client.patch(
            f"/tasks/{task_id}",
            json={},
            headers=headers
        )
        print(response.json())
        assert response.status_code == 400



def test_create_task_invalid_title():
    with TestClient(app) as client:
        token = get_token(client)

        response = client.post(
            "/tasks",
            json={"title": "Test"},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 422


def test_create_task_invalid_title_detail():
    with TestClient(app) as client:
        token = get_token(client)

        response = client.post(
            "/tasks",
            json={"title": "Test"},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 422
        assert response.json()["detail"][0]["loc"] == ["body", "title"]

def test_get_tasks_without_token():
    with TestClient(app) as client:
        response = client.get("/tasks")

        assert response.status_code == 401

def test_get_tasks_invalid_token():
    with TestClient(app) as client:
        response = client.get(
            "/tasks",
            headers={"Authorization": "Bearer invalid_token"}
        )

        assert response.status_code == 401

def test_user_cannot_access_another_users_task():
    with TestClient(app) as client:
        # Создаём первого пользователя
        email_a = f"user_a_{uuid.uuid4().hex}@example.com"
        response = client.post("/users/", json={
            "username": "user_a",
            "email": email_a,
            "password": "TestPassword123!"
        })
        assert response.status_code == 200

        # Создаём второго пользователя
        email_b = f"user_b_{uuid.uuid4().hex}@example.com"
        response = client.post("/users/", json={
            "username": "user_b",
            "email": email_b,
            "password": "TestPassword123!"
        })
        assert response.status_code == 200

        # Получаем токены обоих пользователей
        response = client.post("/users/login", json={
            "email": email_a,
            "password": "TestPassword123!"
        })
        token_a = response.json()["access_token"]

        response = client.post("/users/login", json={
            "email": email_b,
            "password": "TestPassword123!"
        })
        token_b = response.json()["access_token"]

        # Пользователь A создаёт задачу
        headers_a = {"Authorization": f"Bearer {token_a}"}
        response = client.post(
            "/tasks",
            json={"title": "Private task"},
            headers=headers_a
        )
        assert response.status_code == 200
        task_id = response.json()["id"]

        # Пользователь B пытается получить чужую задачу
        headers_b = {"Authorization": f"Bearer {token_b}"}
        response = client.get(f"/tasks/{task_id}", headers=headers_b)

        assert response.status_code == 404

def test_user_cannot_update_another_users_task():
    with TestClient(app) as client:
        email_a = f"user_a_{uuid.uuid4().hex}@example.com"
        email_b = f"user_b_{uuid.uuid4().hex}@example.com"
        password = "TestPassword123!"

        for username, email in [("user_a", email_a), ("user_b", email_b)]:
            response = client.post("/users/", json={
                "username": username,
                "email": email,
                "password": password
            })
            assert response.status_code == 200

        response = client.post("/users/login", json={
            "email": email_a,
            "password": password
        })
        token_a = response.json()["access_token"]

        response = client.post("/users/login", json={
            "email": email_b,
            "password": password
        })
        token_b = response.json()["access_token"]

        response = client.post(
            "/tasks",
            json={"title": "Private task"},
            headers={"Authorization": f"Bearer {token_a}"}
        )
        assert response.status_code == 200
        task_id = response.json()["id"]

        response = client.patch(
            f"/tasks/{task_id}",
            json={"title": "Hacked task"},
            headers={"Authorization": f"Bearer {token_b}"}
        )

        assert response.status_code == 404

def test_user_cannot_delete_another_users_task():
    with TestClient(app) as client:
        email_a = f"user_a_{uuid.uuid4().hex}@example.com"
        email_b = f"user_b_{uuid.uuid4().hex}@example.com"
        password = "TestPassword123!"

        for username, email in [("user_a", email_a), ("user_b", email_b)]:
            response = client.post("/users/", json={
                "username": username,
                "email": email,
                "password": password
            })
            assert response.status_code == 200

        response = client.post("/users/login", json={
            "email": email_a,
            "password": password
        })
        token_a = response.json()["access_token"]

        response = client.post("/users/login", json={
            "email": email_b,
            "password": password
        })
        token_b = response.json()["access_token"]

        response = client.post(
            "/tasks",
            json={"title": "Private task"},
            headers={"Authorization": f"Bearer {token_a}"}
        )
        assert response.status_code == 200
        task_id = response.json()["id"]

        response = client.delete(
            f"/tasks/{task_id}",
            headers={"Authorization": f"Bearer {token_b}"}
        )
        assert response.status_code == 404

        # Проверяем, что задача осталась у пользователя A
        response = client.get(
            f"/tasks/{task_id}",
            headers={"Authorization": f"Bearer {token_a}"}
        )
        assert response.status_code == 200

def test_put_task():
    with TestClient(app) as client:
        token = get_token(client)
        headers = {"Authorization": f"Bearer {token}"}

        response = client.post(
            "/tasks",
            json={"title": "Old title"},
            headers=headers
        )
        assert response.status_code == 200
        task_id = response.json()["id"]

        response = client.put(
            f"/tasks/{task_id}",
            json={"title": "New title", "done": True},
            headers=headers
        )

        assert response.status_code == 200
        assert response.json()["title"] == "New title"
        assert response.json()["done"] is True

def test_user_cannot_put_another_users_task():
    with TestClient(app) as client:
        password = "TestPassword123!"
        email_a = f"user_a_{uuid.uuid4().hex}@example.com"
        email_b = f"user_b_{uuid.uuid4().hex}@example.com"

        for username, email in [("user_a", email_a), ("user_b", email_b)]:
            response = client.post("/users/", json={
                "username": username,
                "email": email,
                "password": password
            })
            assert response.status_code == 200

        response = client.post("/users/login", json={
            "email": email_a,
            "password": password
        })
        token_a = response.json()["access_token"]

        response = client.post("/users/login", json={
            "email": email_b,
            "password": password
        })
        token_b = response.json()["access_token"]

        response = client.post(
            "/tasks",
            json={"title": "Original task"},
            headers={"Authorization": f"Bearer {token_a}"}
        )
        assert response.status_code == 200
        task_id = response.json()["id"]

        response = client.put(
            f"/tasks/{task_id}",
            json={"title": "Changed task", "done": True},
            headers={"Authorization": f"Bearer {token_b}"}
        )

        assert response.status_code == 404

        # Проверяем, что исходная задача не изменилась
        response = client.get(
            f"/tasks/{task_id}",
            headers={"Authorization": f"Bearer {token_a}"}
        )
        assert response.status_code == 200
        assert response.json()["title"] == "Original task"
        assert response.json()["done"] is False

def test_patch_updates_only_title():
    with TestClient(app) as client:
        token = get_token(client)
        headers = {"Authorization": f"Bearer {token}"}

        create_response = client.post(
            "/tasks/",
            json={"title": "Старая задача", "done": True},
            headers=headers,
        )
        assert create_response.status_code == 200

        task_id = create_response.json()["id"]

        response = client.patch(
            f"/tasks/{task_id}",
            json={"title": "Новая задача"},
            headers=headers,
        )
        print("После создания:", create_response.json())
        print("Перед PATCH:", client.get(
            f"/tasks/{task_id}", headers=headers
        ).json())
        assert response.status_code == 200
        assert response.json()["title"] == "Новая задача"
        assert response.json()["done"] is True
