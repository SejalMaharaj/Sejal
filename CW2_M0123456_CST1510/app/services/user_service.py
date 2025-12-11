# app/services/user_service.py

import sqlite3
from pathlib import Path
import bcrypt
from app.data.users import User  # now this exists


class UserService:
    def __init__(self, db_path: str = "DATA/intelligence_platform.db"):
        self.db_path = Path(db_path)

    def _connect(self):
        return sqlite3.connect(self.db_path)

    # REGISTER USER
    def register_user(self, username: str, password: str, role: str = "user"):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            conn.close()
            return False, f"Username '{username}' already exists."

        password_hash = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, password_hash, role)
        )
        conn.commit()
        conn.close()
        return True, f"User '{username}' registered successfully."

    # LOGIN USER
    def authenticate(self, username: str, password: str) -> User | None:
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT username, password_hash, role FROM users WHERE username = ?",
            (username,),
        )
        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        stored_hash = row[1].encode("utf-8")
        if bcrypt.checkpw(password.encode("utf-8"), stored_hash):
            return User(username=row[0], role=row[2])
        return None

    # MIGRATE USERS
    def migrate_users_from_file(self, filepath: Path = Path("DATA/users.txt")):
        if not filepath.exists():
            return 0

        conn = self._connect()
        cursor = conn.cursor()
        migrated_count = 0

        with open(filepath, "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                username, password_hash = line.split(",")

                cursor.execute(
                    "INSERT OR IGNORE INTO users (username, password_hash, role) "
                    "VALUES (?, ?, ?)",
                    (username, password_hash, "user"),
                )

                if cursor.rowcount > 0:
                    migrated_count += 1

        conn.commit()
        conn.close()
        return migrated_count
