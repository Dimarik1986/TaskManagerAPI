from datetime import datetime

from pydantic import BaseModel


class CreateUser(BaseModel):
    username: str
    email: str
    password: str

class ResponseUser(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    is_active: bool


class LoginUser(BaseModel):
    email: str
    password: str
