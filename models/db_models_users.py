from sqlalchemy import Boolean, DateTime, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from models.db_base import Base


class User(Base):
    __tablename__ = "users"

    id:         Mapped[int] = mapped_column(Integer, primary_key=True)
    username:   Mapped[str] = mapped_column(String(100), nullable=False)
    email:      Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash:   Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("true"),
    )