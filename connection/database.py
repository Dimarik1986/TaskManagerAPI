import os
import sqlite3
from pathlib import Path


DB_PATH = Path(
    os.getenv(
        "TASK_MANAGER_DB",
        str(Path(__file__).resolve().parent.parent / "data" / "notes.db")
    )
)


class DatabaseConnection:
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = os.getenv("TASK_MANAGER_DB")

        if db_path is None:
            db_path = (
                Path(__file__).resolve().parent.parent
                / "data"
                / "notes.db"
            )

        self.connection = sqlite3.connect(
            db_path,
            check_same_thread=False
        )
        self.connection.row_factory = None

    def close(self):
        self.connection.close()



