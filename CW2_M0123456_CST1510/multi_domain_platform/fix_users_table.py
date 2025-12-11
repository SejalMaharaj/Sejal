# fix_users_table.py
import sqlite3
from pathlib import Path

DB_PATH = Path("DATA/intelligence_platform.db")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Drop the old users table (with 'password' column)
cur.execute("DROP TABLE IF EXISTS users")

# Recreate users table with password_hash column
cur.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

conn.commit()
conn.close()
print("Users table recreated with password_hash column.")
