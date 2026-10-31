from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.db_models_tasks import Task


class TasksDB:
    def __init__(self, db: Session):
        self.db = db

    def add_task(self, title, user_id, done):
        new_task = Task(
            title=title,
            done=done,
            user_id=user_id
        )
        try:
            self.db.add(new_task)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise
        return new_task

    def get_tasks(self, user_id: int):
        return self.db.query(Task).filter(Task.user_id==user_id).all()

    def get_task(self, task_id:int, user_id: int):
        return self.db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()

    def delete_task(self, task_id: int, user_id: int):
        task = self.db.query(Task).filter( Task.id==task_id,Task.user_id==user_id).first()
        if task:
            self.db.delete(task)
            self.db.commit()
            return True
        else:
            return False

    def update_task(self, task_id, title, done, user_id):
        up_task = self.db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
        if up_task:
            up_task.title = title
            up_task.done = done
            self.db.commit()
            return True
        return False

    def patch_task(self, task_id: int, user_id: int, changes: dict):
        task = self.db.query(Task).filter(
            Task.id == task_id,
            Task.user_id == user_id
        ).first()

        if task is None:
            return None

        allowed_fields = {"title", "done"}

        for key, value in changes.items():
            if key in allowed_fields:
                setattr(task, key, value)

        self.db.commit()
        self.db.refresh(task)

        return task