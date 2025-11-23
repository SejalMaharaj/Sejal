# app/services/user_service.py

import sqlite3
from pathlib import Path
import bcrypt
from app.data.db import connect_database
from app.data.users import get_user_by_username, insert_user

DATA_DIR = Path("DATA")  # Path to DATA folder


def register_user(conn, username, password, role="user"):
    """
    Register a new user in the database with hashed password.

    Args:
        conn: Database connection
        username: User's login name
        password: Plain text password
        role: User role (default 'user')

    Returns:
        tuple: (success: bool, message: str)
    """
    cursor = conn.cursor()

    # Check if user already exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        return False, f"Username '{username}' already exists."

    # Hash the password
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    password_hash = hashed.decode('utf-8')

    # Insert new user
    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, role)
    )
    conn.commit()
    return True, f"User '{username}' registered successfully!"


def login_user(conn, username, password):
    """
    Authenticate a user against the database.

    Args:
        conn: Database connection
        username: User's login name
        password: Plain text password

    Returns:
        tuple: (success: bool, message: str)
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if not user:
        return False, "Username not found."

    stored_hash = user[2]  # password_hash column
    password_bytes = password.encode('utf-8')
    hash_bytes = stored_hash.encode('utf-8')

    if bcrypt.checkpw(password_bytes, hash_bytes):
        return True, f"Welcome, {username}!"
    else:
        return False, "Invalid password."


def migrate_users_from_file(conn, filepath=DATA_DIR / "users.txt"):
    """
    Migrate users from users.txt to the database.

    Args:
        conn: Database connection
        filepath: Path to users.txt file
    """
    if not filepath.exists():
        print(f"File not found: {filepath}")
        print("   No users to migrate.")
        return 0

    cursor = conn.cursor()
    migrated_count = 0

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Parse line: username,password_hash
            parts = line.split(',')
            if len(parts) >= 2:
                username = parts[0]
                password_hash = parts[1]

                # Insert user (ignore if already exists)
                try:
                    cursor.execute(
                        "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                        (username, password_hash, 'user')
                    )
                    if cursor.rowcount > 0:
                        migrated_count += 1
                except sqlite3.Error as e:
                    print(f"Error migrating user {username}: {e}")

    conn.commit()
    print(f"Migrated {migrated_count} users from {filepath.name}")
    return migrated_count
