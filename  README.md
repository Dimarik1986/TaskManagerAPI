# TaskManagerAPI

REST API for task management built with Python and FastAPI.

## Features

- User registration and authentication
- JWT-based authentication
- Password hashing
- Create, read, update, and delete tasks
- Partial task updates with PATCH
- User-specific task isolation
- SQLite database
- Automated API tests with pytest

## Tech Stack

- Python
- FastAPI
- Pydantic
- SQLite
- PyJWT
- Argon2
- pytest

## Installation

Clone the repository:

```bash
git clone https://github.com/Dimarik1986/TaskManagerAPI.git
cd TaskManagerAPI
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Configure the JWT secret using a local secret file or an environment variable, according to the application's configuration.

Do not commit secrets or local database files to the repository.

## Run the Application

```bash
uvicorn server.fast_api_server:app --reload
```

Open the interactive API documentation at:

`http://127.0.0.1:8000/docs`

## Run Tests

```bash
python -m pytest -v
```

## Project Structure

- `server/` — FastAPI application setup
- `routers/` — API endpoints
- `managers/` — task and user management logic
- `database/` — database operations
- `connection/` — database connection
- `models/` — data schemas and models
- `function/` — security and helper functions
- `tests/` — automated tests

## Status

This project is under active development as a backend portfolio project.
