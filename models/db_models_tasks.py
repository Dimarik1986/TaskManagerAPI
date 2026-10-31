from sqlalchemy import Boolean, ForeignKey, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from models.db_base import Base


class Task(Base):
    __tablename__ = "tasks"

    id:         Mapped[int] = mapped_column(Integer, primary_key=True)
    title:      Mapped[str] = mapped_column(String(255), nullable=False)
    done:       Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    user_id:    Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )