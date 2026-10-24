import os
from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash
from function.users_function import open_file

pwd_hash = PasswordHash.recommended()


def create_user_hash(password: str) -> str:
    hashed_password = pwd_hash.hash(password)
    return hashed_password


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_hash.verify(password, hashed_password)


import os

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    try:
        SECRET_KEY = open_file("secret.txt")
    except FileNotFoundError:
        if os.getenv("GITHUB_ACTIONS") == "true":
            SECRET_KEY = "test-only-secret-key-for-ci"
        else:
            raise RuntimeError(
                "SECRET_KEY is not configured and secret.txt was not found"
            )

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(user_id: int):
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])