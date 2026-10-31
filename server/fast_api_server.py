
from contextlib import asynccontextmanager
from fastapi import FastAPI

from routers import tasks, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(tasks.router)
app.include_router(users.router)
