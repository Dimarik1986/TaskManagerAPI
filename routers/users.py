from sqlalchemy.exc import IntegrityError
import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm.session import Session

from connection.postgres_depency import get_db
from database.users_db_sqlalchemy import UsersDB
from function.security import decode_access_token

from fastapi import APIRouter, HTTPException, Depends, Request, Response, status

from function.security import verify_password, create_access_token
from managers.usersManage import UsersManager
from models.db_models_users import User

from models.users import ResponseUser, CreateUser, LoginUser

router = APIRouter(prefix="/users", tags=["Users"])


def get_manager(db:Session=Depends(get_db)):
    return UsersManager(UsersDB(db))

@router.post("/", response_model=ResponseUser)
async def add_user(users: CreateUser, manager: UsersManager = Depends(get_manager)):
    try:
        request_user = manager.add_user(users)
    except IntegrityError as e:
        print("\nREAL DATABASE ERROR:", repr(e.orig))
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e.orig)
        )
    return request_user

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme)
) -> int:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    try:
        payload = decode_access_token(token)
        user_id = int(payload["sub"])
    except (jwt.InvalidTokenError, KeyError, TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id


@router.get("/me", response_model=ResponseUser)
async def get_current_user(
    user_id: int = Depends(get_current_user_id),
    manager: UsersManager = Depends(get_manager),
):
    user = manager.get_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user

@router.get("/{user_id}", response_model=ResponseUser)
async def get_user(user_id: int, manager: UsersManager = Depends(get_manager)):
    response_user = manager.get_user(user_id)
    if response_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return response_user

@router.get("/", response_model=list[ResponseUser])
async def get_users(manager: UsersManager = Depends(get_manager)):
    return manager.get_users()

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, manager: UsersManager = Depends(get_manager)):
    user = manager.delete_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{user_id}", response_model=ResponseUser)
async def update_user(user_id: int,users: CreateUser, manager: UsersManager = Depends(get_manager)):
    user = manager.update_user(users, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return manager.get_user(user_id)


@router.post("/login")
async def login(users: LoginUser,
    manager: UsersManager = Depends(get_manager)
):
    user = manager.get_user_by_email(users.email)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(users.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return  {
        "access_token": create_access_token(user.id),
        "token_type": "bearer"
            }




