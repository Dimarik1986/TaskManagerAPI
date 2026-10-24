def response_user(user):
    user_response = {
        "id": user[0],
        "username": user[1],
        "email": user[2],
        "created_at": user[4],
        "is_active": user[5],
    }
    return user_response

def response_users(users: list):
    return [response_user(user) for user in users]

from pathlib import Path


def open_file(filename):
    file_path = Path(__file__).resolve().parent.parent / filename

    with open(file_path, encoding="utf-8") as f:
        return f.read().strip()
