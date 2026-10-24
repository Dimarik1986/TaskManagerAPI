

from function.task_function import response_task, response_tasks


class TasksDB:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def create_table(self):
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS Tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done BOOLEAN NOT NULL DEFAULT 0,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES Users(id)
            )
        """)
        self.connection.commit()


    def add_task(self, title, user_id, done):
        self.cursor.execute('INSERT INTO Tasks (title, user_id, done) values (?, ?, ?)', (title,user_id, done))
        generated_id = self.cursor.lastrowid
        self.cursor.execute('SELECT * FROM Tasks WHERE id = ? AND user_id = ?', (generated_id,user_id,))
        task = self.cursor.fetchone()
        self.connection.commit()
        task_response = response_task(task)
        return task_response


    def get_tasks(self, user_id):
        self.cursor.execute('SELECT * FROM Tasks WHERE user_id = ?',(user_id,))
        tasks = self.cursor.fetchall()
        tasks_response = response_tasks(tasks)
        return tasks_response


    def get_task(self, task_id, user_id):
        self.cursor.execute('SELECT * FROM Tasks WHERE id = ? AND user_id = ?', (task_id, user_id))
        task = self.cursor.fetchone()
        if task is None:
            return None
        return response_task(task)


    def delete_task(self, task_id, user_id):
        self.cursor.execute('DELETE FROM Tasks WHERE id = ? AND user_id = ?', (task_id,user_id,))
        is_deleted = self.cursor.rowcount > 0
        self.connection.commit()
        return is_deleted


    def update_task(self, task_id, title, done, user_id):
        self.cursor.execute('UPDATE Tasks SET title = ?, done = ? WHERE id = ? AND user_id = ?', (title, done, task_id, user_id,))
        is_updated = self.cursor.rowcount > 0
        self.connection.commit()
        return is_updated


    def patch_task(self, task_id, user_id, changes):
        allowed_fields = {"title", "done"}

        fields = {
            key: value
            for key, value in changes.items()
            if key in allowed_fields
        }

        if not fields:
            return self.get_task(task_id, user_id)

        set_clause = ", ".join(
            [f"{key} = ?" for key in fields]
        )

        values = list(fields.values()) + [task_id] + [user_id]

        self.cursor.execute(
            f"UPDATE Tasks SET {set_clause} WHERE id = ? AND user_id = ?",
            values
        )

        self.connection.commit()

        return self.get_task(task_id, user_id)