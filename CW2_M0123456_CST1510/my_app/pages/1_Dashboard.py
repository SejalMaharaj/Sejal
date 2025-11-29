# 1_Dashboard.py
import streamlit as st
from db import connect_database
import pandas as pd

st.set_page_config(page_title="Main Dashboard", page_icon="📊", layout="wide")

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = None

# Guard: Only logged-in users can access
if not st.session_state.logged_in:
    st.error("You must be logged in to view the dashboard.")
    if st.button("Go to Login Page"):
        st.switch_page("home.py")
    st.stop()

# ---------------- MAIN DASHBOARD ----------------
st.title("📊 Main Dashboard")
st.success(f"Hello, **{st.session_state.username}**! You are logged in as **{st.session_state.role}**.")

st.caption("Use the buttons below to go to your role-specific dashboard.")

# ---------------- ROLE-BASED NAVIGATION ----------------
if st.session_state.role == "cyber":
    if st.button("🔐 Go to Cybersecurity Dashboard"):
        st.switch_page("pages/2_Cybersecurity.py")

elif st.session_state.role == "datascience":
    if st.button("📈 Go to Data Science Dashboard"):
        st.switch_page("pages/3_DataScience.py")

elif st.session_state.role == "itops":
    if st.button("🛠️ Go to IT Operations Dashboard"):
        st.switch_page("pages/4_IT_Operations.py")

# ---------------- DASHBOARD SUMMARY EXAMPLE ----------------
st.subheader("Quick Data Overview (Demo)")

# Connect to database
conn = connect_database()

# Show some summary counts
try:
    cyber_count = pd.read_sql("SELECT COUNT(*) as count FROM cyber_incidents", conn).iloc[0]["count"]
    ds_count = pd.read_sql("SELECT COUNT(*) as count FROM datasets", conn).iloc[0]["count"]
    it_count = pd.read_sql("SELECT COUNT(*) as count FROM it_tickets", conn).iloc[0]["count"]
except Exception as e:
    st.warning(f"Error loading summary data: {e}")
    cyber_count = ds_count = it_count = 0

conn.close()

col1, col2, col3 = st.columns(3)
col1.metric("Total Cyber Incidents", cyber_count)
col2.metric("Total Datasets", ds_count)
col3.metric("Total IT Tickets", it_count)

# ---------------- LOGOUT BUTTON ----------------
st.divider()
if st.button("Log Out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = None
    st.info("You have been logged out.")
    st.switch_page("home.py")
