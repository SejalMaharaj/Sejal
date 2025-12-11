import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from app.services.user_service import UserService
from multi_domain_platform.database.db import connect_database
from app.data.users import create_users_table

# make sure DB and users table exist
conn_init = connect_database()
create_users_table(conn_init)
conn_init.close()

user_service = UserService()

# Page config
st.set_page_config(page_title="Login / Register", page_icon="🔑", layout="centered")
st.title("🔐 Welcome to Intelligence Platform")


# Create service object (OOP)
user_service = UserService()

# -----------------------------
# Session state
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = None
if "user" not in st.session_state:
    st.session_state.user = None

# -----------------------------
# Already logged in
# -----------------------------
if st.session_state.logged_in:
    st.success(f"Already logged in as **{st.session_state.username}**!")
    if st.button("Go to Dashboard"):
        st.switch_page("pages/1_Dashboard.py")
    st.stop()

# -----------------------------
# Tabs
# -----------------------------
tab_login, tab_register = st.tabs(["Login", "Register"])

# -----------------------------
# LOGIN TAB
# -----------------------------
with tab_login:
    st.subheader("Login")
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Log in", type="primary"):
        user = user_service.authenticate(login_username, login_password)
        if user:
            st.session_state.logged_in = True
            st.session_state.username = user.username
            st.session_state.role = user.role
            st.success(f"Welcome back, {user.username}! 🎉")
            st.switch_page("pages/1_Dashboard.py")
        else:
            st.error("Invalid username or password.")


# -----------------------------
# REGISTER TAB
# -----------------------------
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
            ok, msg = user_service.register_user(new_username, new_password, role)
            if ok:
                st.success(msg)
                st.info("Go to the Login tab and sign in with your new account.")
            else:
                st.error(msg)
