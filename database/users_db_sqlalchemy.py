from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from models.db_models_users import User
from models.users import CreateUser


class UsersDB:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def add_user(self, user: dict[str, str]):
        new_user = User(
            username=user["username"],
            email=user["email"],
            password_hash=user["password_hash"],
        )

        try:
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
        except IntegrityError:
            self.db.rollback()
            raise
        return new_user


    def delete_user(self, user_id: int):
        user = self.db.get(User, user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        else:
            return False

    def get_users(self):
        return self.db.query(User).all()

    def update_user(self, user: CreateUser, user_id: int):
        up_user = self.db.get(User, user_id)

        if up_user is None:
            return False

        up_user.username = user.username
        up_user.email = user.email

        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise

        return True