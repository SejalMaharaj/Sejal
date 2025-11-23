import bcrypt
import os
import re


def hash_password(plain_text_password):
    password_bytes = plain_text_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))


def register_user(username, password):
    if not validate_username(username):
        print("Invalid username. It must be at least 4 characters, can contain only letters/numbers.")
        return False

    if not validate_password(password):
        print("Weak password. It must be at least 8 characters and include upper, lower, number, and symbol.")
        return False

    if user_exists(username):
        print("Username already exists. Try a different one.")
        return False

    hashed_password = hash_password(password)

    with open("../../DATA/users.txt", "a") as f:
        f.write(f"{username},{hashed_password}\n")

    print(f"User '{username}' registered successfully!")
    return True


def login_user(username, password):
    if not os.path.exists("../../DATA/users.txt"):
        print("No users registered yet.")
        return False

    with open("../../DATA/users.txt", "r") as f:
        for line in f:
            stored_user, stored_hash = line.strip().split(',', 1)
            if stored_user == username:
                if verify_password(password, stored_hash):
                    print(f"Login successful, {username}.")
                    return True
                else:
                    print("Incorrect password.")
                    return False
    print("Username not found.")
    return False


def user_exists(username):
    if not os.path.exists("../../DATA/users.txt"):
        return False
    with open("../../DATA/users.txt", "r") as f:
        for line in f:
            stored_user, _ = line.strip().split(',', 1)
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


def main():
    while True:
        print("1. Register")
        print("2. Log in")
        print("3. Exit")



        choice = input("Enter your choice (1–3): ")

        if choice == "1":
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            register_user(username, password)

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









