from fastapi import APIRouter, HTTPException, Depends, Request, Response, status

from connection.postgres_depency import get_db
from sqlalchemy.orm import Session
from database.tasks_db_sqlalchemy import TasksDB
from managers.taskManage import TaskManage
from models.tasks import TaskResponse, TaskCreate, TaskPatch
from routers.users import get_current_user_id

router = APIRouter(prefix="/tasks", tags=["Tasks"])

def get_manager(db:Session=Depends(get_db)):
    return TaskManage(TasksDB(db))


@router.get("", response_model=list[TaskResponse])
async def tasks(
        user_id: int = Depends(get_current_user_id),
        manager: TaskManage = Depends(get_manager),
    ):
    return manager.get_tasks(user_id)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
        task_id: int,
        user_id: int = Depends(get_current_user_id),
        manager: TaskManage = Depends(get_manager)

        ):
    task = manager.get_task(task_id, user_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("", response_model=TaskResponse)
async def add_task(
        data: TaskCreate,
        user_id: int = Depends(get_current_user_id),
        manager: TaskManage = Depends(get_manager)
        ):
    task = manager.add_task(
        data.title,
        user_id,
        data.done,
    )
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
        task_id: int,
        user_id: int = Depends(get_current_user_id),
        manager: TaskManage = Depends(get_manager)
        ):

    task = manager.delete_task(task_id, user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
        task_id: int,
        title: TaskCreate,
        user_id: int = Depends(get_current_user_id),
        manager: TaskManage = Depends(get_manager)
        ):
    my_json = title.title
    task = manager.update_task(task_id, my_json, title.done, user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return manager.get_task(task_id, user_id)



@router.patch("/{task_id}", response_model=TaskResponse)
def patch_task(
    task_id: int,
    data: TaskPatch,
    user_id: int = Depends(get_current_user_id),
    manager: TaskManage = Depends(get_manager),
):
    changes = data.model_dump(exclude_unset=True)

    if not changes:
        raise HTTPException(
            status_code=400,
            detail="No fields to update",
        )

    task = manager.patch_task(task_id, user_id, changes)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return task