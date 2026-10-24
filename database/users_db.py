import sqlite3
from sqlite3 import IntegrityError

from function.users_function import response_user, response_users
from models.users import CreateUser


class UsersDB:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()


    def create_table_users(self):
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN NOT NULL DEFAULT 1)
                """)

        self.connection.commit()

    def add_user(self, user: dict):
        try:
            self.cursor.execute(
                """INSERT INTO Users (username, email, password_hash)
                VALUES (?, ?, ?)""",
                (user["username"], user["email"], user["password_hash"])
            )
        except sqlite3.IntegrityError:
            self.connection.rollback()
            raise

        generated_id = self.cursor.lastrowid
        self.cursor.execute('SELECT * FROM Users WHERE id = ?', (generated_id,))
        user = self.cursor.fetchone()
        self.connection.commit()
        user_response = response_user(user)
        return user_response

    def get_user(self, user_id: int):
        self.cursor.execute('SELECT * FROM Users WHERE id = ?', (user_id,))
        user = self.cursor.fetchone()
        if user is None:
            return None
        else:
            user_response = response_user(user)
        return user_response

    def get_users(self):
        self.cursor.execute('SELECT * FROM Users')
        users = self.cursor.fetchall()
        users_response = response_users(users)
        self.connection.commit()
        return users_response

    def delete_user(self, user_id: int):
        self.cursor.execute('DELETE FROM Users WHERE id = ?', (user_id,))
        is_deleted = self.cursor.rowcount > 0
        self.connection.commit()
        return is_deleted

    def update_user(self, user: CreateUser, user_id: int):
        self.cursor.execute('UPDATE Users SET username = ?, email = ? WHERE id = ?',(user.username, user.email, user_id)
                            )
        is_updated = self.cursor.rowcount > 0
        self.connection.commit()
        return is_updated

    def get_user_by_email(self, email: str):
        self.cursor.execute(
            "SELECT * FROM Users WHERE email = ?",
            (email,)
        )
        return self.cursor.fetchone()
