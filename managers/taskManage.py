
class TaskManage:
    def __init__(self,task_db):
        self.task_db = task_db

    def add_task(self, title, user_id, done):
        return self.task_db.add_task(title, user_id, done)

    def get_tasks(self, user_id):
        return self.task_db.get_tasks(user_id)

    def get_task(self, task_id, user_id):
        return self.task_db.get_task(task_id, user_id)

    def delete_task(self, task_id, user_id):
        return self.task_db.delete_task(task_id, user_id)

    def update_task(self, task_id, title, done, user_id):
        return self.task_db.update_task(task_id, title, done, user_id)

    def patch_task(self, task_id, user_id, changes):
        return self.task_db.patch_task(task_id, user_id, changes)