from function.security import create_user_hash
from models.users import CreateUser


class UsersManager:
    def __init__(self,user_db):
        self.user_db = user_db

    def add_user(self, user: CreateUser):
        hashed_password = create_user_hash(user.password)

        user_data = user.model_dump()
        user_data.pop("password")
        user_data["password_hash"] = hashed_password

        return self.user_db.add_user(user_data)

    def get_user(self,user_id: int):
        return self.user_db.get_user(user_id)

    def get_users(self):
        return self.user_db.get_users()

    def delete_user(self,user_id: int):
        return self.user_db.delete_user(user_id)
    def update_user(self,user: CreateUser,user_id: int):
        return self.user_db.update_user(user, user_id)
    def get_user_by_email(self,email: str):
        return self.user_db.get_user_by_email(email)