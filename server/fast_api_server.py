from contextlib import asynccontextmanager
from fastapi import FastAPI

from connection.database import DatabaseConnection

from database.tasks_db import TasksDB
from database.users_db import UsersDB
from routers import tasks, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = DatabaseConnection()
    tasks_db = TasksDB(db.connection)
    users_db = UsersDB(db.connection)
    users_db.create_table_users()
    tasks_db.create_table()


    app.state.db = db
    app.state.tasks_db = tasks_db
    app.state.users_db = users_db

    yield

    db.close()


app = FastAPI(lifespan=lifespan)
app.include_router(tasks.router)
app.include_router(users.router)