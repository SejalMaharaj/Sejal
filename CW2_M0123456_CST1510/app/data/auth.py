import os
import re
import bcrypt
import time
import secrets
import json

# ---------------- Paths ----------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "DATA")
USERS_FILE = os.path.join(DATA_DIR, "users.txt")
FAILED_ATTEMPTS_FILE = os.path.join(DATA_DIR, "failed_attempts.txt")
LOCKOUT_DURATION = 300  # 5 minutes in seconds

# Ensure DATA directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# ---------------- Original functions ----------------
def hash_password(plain_text_password):
    password_bytes = plain_text_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))


def register_user(username, password, role="user"):
    if not validate_username(username):
        print("Invalid username. It must be at least 4 characters, letters/numbers only.")
        return False

    if not validate_password(password):
        print("Weak password. It must be at least 8 characters and include upper, lower, number, and symbol.")
        return False

    if user_exists(username):
        print("Username already exists. Try a different one.")
        return False

    hashed_password = hash_password(password)

    with open(USERS_FILE, "a") as f:
        f.write(f"{username},{hashed_password},{role}\n")

    print(f"User '{username}' with role '{role}' registered successfully!")
    return True


def login_user(username, password):
    if not os.path.exists(USERS_FILE):
        print("No users registered yet.")
        return False

    if is_locked(username):
        print(f"Account '{username}' is temporarily locked. Try later.")
        return False

    with open(USERS_FILE, "r") as f:
        for line in f:
            stored_user, stored_hash, *_ = line.strip().split(',', 2)
            if stored_user == username:
                if verify_password(password, stored_hash):
                    print(f"Login successful, {username}.")
                    reset_failed_attempts(username)
                    session_token = create_session(username)
                    print(f"Session token: {session_token}")
                    return True
                else:
                    record_failed_attempt(username)
                    return False
    print("Username not found.")
    return False


def user_exists(username):
    if not os.path.exists(USERS_FILE):
        return False
    with open(USERS_FILE, "r") as f:
        for line in f:
            stored_user = line.strip().split(',', 1)[0]
            if stored_user == username:
                return True
    return False


def validate_username(username):
    pattern = r"^[A-Za-z0-9]{4,}$"
    if re.match(pattern, username):
        print("Username passed.")
        return True
    else:
        print("Username failed")
        return False


def validate_password(password):
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    if re.match(pattern, password):
        print("Password passed")
        return True
    else:
        print("Password failed")
        return False

# ---------------- Challenge 3: Account Lockout with warning ----------------
def record_failed_attempt(username):
    attempts = load_failed_attempts()
    if username not in attempts:
        attempts[username] = {"count": 1, "first_attempt": time.time()}
        print(f"Warning: 2 tries left before account is locked.")
    else:
        attempts[username]["count"] += 1
        remaining_tries = 3 - attempts[username]["count"]
        if attempts[username]["count"] < 3:
            print(f"Warning: {remaining_tries} {'try' if remaining_tries == 1 else 'tries'} left before account is locked.")
        else:
            attempts[username]["lock_time"] = time.time()
            print(f"Account '{username}' locked for 5 minutes due to multiple failed attempts.")
    save_failed_attempts(attempts)


def is_locked(username):
    attempts = load_failed_attempts()
    if username in attempts and "lock_time" in attempts[username]:
        elapsed = time.time() - attempts[username]["lock_time"]
        if elapsed < LOCKOUT_DURATION:
            return True
        else:
            # Unlock after duration
            attempts[username]["count"] = 0
            del attempts[username]["lock_time"]
            save_failed_attempts(attempts)
    return False


def reset_failed_attempts(username):
    attempts = load_failed_attempts()
    if username in attempts:
        attempts[username]["count"] = 0
        if "lock_time" in attempts[username]:
            del attempts[username]["lock_time"]
        save_failed_attempts(attempts)


def load_failed_attempts():
    if not os.path.exists(FAILED_ATTEMPTS_FILE):
        return {}
    with open(FAILED_ATTEMPTS_FILE, "r") as f:
        return json.load(f)


def save_failed_attempts(attempts):
    with open(FAILED_ATTEMPTS_FILE, "w") as f:
        json.dump(attempts, f)

# ---------------- Challenge 4: Session Management ----------------
def create_session(username):
    token = secrets.token_hex(16)
    # Can be extended to store session tokens if needed
    return token

# ---------------- Main loop ----------------
def main():
    while True:
        print("\n1. Register")
        print("2. Log in")
        print("3. Exit")

        choice = input("Enter your choice (1–3): ")

        if choice == "1":
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            role = input("Enter role (user/admin/analyst) [default: user]: ") or "user"
            register_user(username, password, role)

        elif choice == "2":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            login_user(username, password)

        elif choice == "3":
            print("Exiting program.")
            break

        else:
            print("Invalid option. Please choose between 1–3.")


if __name__ == "__main__":
    main()
