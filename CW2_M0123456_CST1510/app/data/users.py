# app/data/users.py
import sqlite3

def create_users_table(conn):
    """Create users table if it doesn't exist."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    print("Users table created successfully!")


def get_user_by_username(conn, username):
    """
    Retrieve user by username.

    Args:
        conn: Database connection
        username: The username to query

    Returns:
        tuple: User record (id, username, password_hash, role, created_at) or None
    """
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )
    return cursor.fetchone()


def insert_user(conn, username, password_hash, role='user'):
    """
    Insert new user into the database.

    Args:
        conn: Database connection
        username: Username
        password_hash: Hashed password
        role: User role (default 'user')
    """
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, role)
    )
    conn.commit()
