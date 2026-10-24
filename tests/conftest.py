import os
import tempfile

import pytest
from fastapi.testclient import TestClient

from server.fast_api_server import app


@pytest.fixture(autouse=True)
def test_database():
    with tempfile.TemporaryDirectory() as temp_dir:
        os.environ["TASK_MANAGER_DB"] = os.path.join(
            temp_dir, "test.db"
        )

        with TestClient(app) as client:
            response = client.post("/users/", json={
                "username": "pytest_user",
                "email": "pytest_user@example.com",
                "password": "TestPassword123!"
            })

            assert response.status_code == 200
            yield

        os.environ.pop("TASK_MANAGER_DB", None)