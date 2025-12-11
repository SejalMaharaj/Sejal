# my_app/pages/1_Dashboard.py

import streamlit as st
import pandas as pd
from db import connect_database

# Page config
st.set_page_config(
    page_title="Main Dashboard",
    page_icon="📊",
    layout="wide",
)

# ---------------- SESSION STATE SETUP ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = None

# ---------------- GUARD: REQUIRE LOGIN ----------------
if not st.session_state.logged_in:
    st.error("You must be logged in to view the dashboard.")
    if st.button("Go to login page"):
        st.switch_page("home.py")
    st.stop()

username = st.session_state.username
role = st.session_state.role

# ---------------- SIDEBAR NAVIGATION ----------------
with st.sidebar:
    st.title("Navigation")

    st.markdown(f"**User:** {username}")
    st.markdown(f"**Role:** {role}")

    st.markdown("---")

    if st.button("Home", use_container_width=True):
        st.switch_page("home.py")

    if st.button("Cybersecurity", use_container_width=True):
        st.switch_page("pages/2_Cybersecurity.py")

    if st.button("Data Science", use_container_width=True):
        st.switch_page("pages/3_DataScience.py")

    if st.button("IT Operations", use_container_width=True):
        st.switch_page("pages/4_IT_Operations.py")

    if st.button("Open AI assistant 🤖", use_container_width=True):
        st.switch_page("pages/AI_assistant.py")

# ---------------- MAIN DASHBOARD ----------------
st.title("📊 Main Dashboard")
st.success(f"Hello, **{username}**! You are logged in as **{role}**.")

st.caption("Use the buttons below to go to your role specific dashboard.")

# ---------------- ROLE BASED NAVIGATION BUTTONS ----------------
if role == "cyber":
    if st.button("🔐 Go to Cybersecurity dashboard"):
        st.switch_page("pages/2_Cybersecurity.py")

elif role == "datascience":
    if st.button("📈 Go to Data Science dashboard"):
        st.switch_page("pages/3_DataScience.py")

elif role == "itops":
    if st.button("🛠️ Go to IT Operations dashboard"):
        st.switch_page("pages/4_IT_Operations.py")

# ---------------- DASHBOARD SUMMARY ----------------
st.subheader("Quick data overview")

conn = connect_database()

try:
    cyber_count = pd.read_sql(
        "SELECT COUNT(*) AS count FROM cyber_incidents", conn
    ).iloc[0]["count"]

    ds_count = pd.read_sql(
        "SELECT COUNT(*) AS count FROM datasets", conn
    ).iloc[0]["count"]

    it_count = pd.read_sql(
        "SELECT COUNT(*) AS count FROM it_tickets", conn
    ).iloc[0]["count"]

except Exception as e:
    st.warning(f"Error loading summary data: {e}")
    cyber_count = ds_count = it_count = 0

conn.close()

col1, col2, col3 = st.columns(3)
col1.metric("Total cyber incidents", cyber_count)
col2.metric("Total datasets", ds_count)
col3.metric("Total IT tickets", it_count)

# ---------------- LOGOUT BUTTON ----------------
st.divider()
if st.button("Log out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = None
    st.info("You have been logged out.")
    st.switch_page("home.py")
