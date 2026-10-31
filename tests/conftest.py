import os
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))


from server.fast_api_server import app
from sqlalchemy import create_engine, text
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from connection.postgres_depency import get_db

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+psycopg://localhost/taskmanager_test"
)

if not TEST_DATABASE_URL.endswith("/taskmanager_test"):
    raise RuntimeError("Unsafe test database URL")

test_engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
)


@pytest.fixture(autouse=True)
def test_database():

    with test_engine.begin() as connection:
        db_name = connection.execute(
            text("SELECT current_database()")
        ).scalar()

        print(f"\nTEST ENGINE DATABASE: {db_name}")

        connection.execute(
            text("TRUNCATE TABLE tasks, users RESTART IDENTITY CASCADE")
        )

    def override_get_db():
        db = TestingSessionLocal()
        try:
            db_name = db.execute(
                text("SELECT current_database()")
            ).scalar()

            print(f"\nAPI DATABASE: {db_name}")
            print("TEST DATABASE DEPENDENCY CALLED")

            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        response = client.post(
            "/users/",
            json={
                "username": "pytest_user",
                "email": "pytest_user@example.com",
                "password": "TestPassword123!",
            },
        )

        assert response.status_code == 200, response.text

        yield client

    app.dependency_overrides.clear()
