# home.py
import streamlit as st
import sqlite3
from db import connect_database

st.set_page_config(page_title="Login / Register", page_icon="🔑", layout="centered")
st.title("🔐 Welcome to Intelligence Platform")

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = None

# ---------------- DATABASE TABLE FOR USERS ----------------
conn = connect_database()
cursor = conn.cursor()

# Create users table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)
""")
conn.commit()

# ---------------- REDIRECT IF LOGGED IN ----------------
if st.session_state.logged_in:
    st.success(f"Already logged in as **{st.session_state.username}**!")
    if st.button("Go to Dashboard"):
        st.session_state.logged_in = True
        st.switch_page("pages/1_Dashboard.py")
    st.stop()

# ---------------- TABS ----------------
tab_login, tab_register = st.tabs(["Login", "Register"])

# ---------------- LOGIN TAB ----------------
with tab_login:
    st.subheader("Login")
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Log in", type="primary"):
        cursor.execute("SELECT password, role FROM users WHERE username = ?", (login_username,))
        result = cursor.fetchone()
        if result and result[0] == login_password:
            st.session_state.logged_in = True
            st.session_state.username = login_username
            st.session_state.role = result[1]
            st.success(f"Welcome back, {login_username}! 🎉")
            st.switch_page("pages/1_Dashboard.py")
        else:
            st.error("Invalid username or password.")

# ---------------- REGISTER TAB ----------------
with tab_register:
    st.subheader("Register")
    new_username = st.text_input("Choose a username", key="register_username")
    new_password = st.text_input("Choose a password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm password", type="password", key="register_confirm")
    role = st.selectbox("Select your role", ["cyber", "datascience", "itops"])

    if st.button("Create account"):
        if not new_username or not new_password:
            st.warning("Please fill in all fields.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        else:
            try:
                cursor.execute(
                    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    (new_username, new_password, role)
                )
                conn.commit()
                st.success("Account created! You can now log in from the Login tab.")
                st.info("Tip: go to the Login tab and sign in with your new account.")
            except sqlite3.IntegrityError:
                st.error("Username already exists. Choose another one.")

# ---------------- CLOSE DB ----------------
conn.close()
