from pathlib import Path
import sqlite3


class DatabaseManager:
    def __init__(self, db_path: str = "DATA/intelligence_platform.db"):
        self.db_path = Path(db_path)

    def connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def execute(self, sql: str, params: tuple = ()):
        with self.connect() as conn:
            cur = conn.cursor()
            cur.execute(sql, params)
            conn.commit()
            return cur
