# 2_Cybersecurity.py
import streamlit as st
import pandas as pd
from db import connect_database

st.set_page_config(page_title="Cybersecurity Dashboard", page_icon="🔐", layout="wide")

# ---------------- SESSION CHECK ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = None

# Guard: only accessible to logged-in Cybersecurity users
if not st.session_state.logged_in or st.session_state.role != "cyber":
    st.error("You must be logged in as a Cybersecurity user to view this page.")
    if st.button("Go to Login Page"):
        st.switch_page("home.py")
    st.stop()

# ---------------- DASHBOARD ----------------
st.title("🔐 Cybersecurity Dashboard")
st.success(f"Hello, **{st.session_state.username}**! You are logged in as Cybersecurity.")

# ---------------- DATABASE ----------------
conn = connect_database()
cyber_df = pd.read_sql("SELECT * FROM cyber_incidents", conn)
conn.close()

# ---------------- INLINE FILTERS ----------------
st.subheader("Filter Incidents")
col1, col2, col3 = st.columns(3)

with col1:
    severity_filter = st.selectbox(
        "Select Severity",
        options=["All"] + list(cyber_df["severity"].unique())
    )

with col2:
    status_filter = st.selectbox(
        "Select Status",
        options=["All"] + list(cyber_df["status"].unique())
    )

with col3:
    category_filter = st.selectbox(
        "Select Category",
        options=["All"] + list(cyber_df["category"].unique())
    )

# Apply filters
filtered_df = cyber_df.copy()

if severity_filter != "All":
    filtered_df = filtered_df[filtered_df["severity"] == severity_filter]

if status_filter != "All":
    filtered_df = filtered_df[filtered_df["status"] == status_filter]

if category_filter != "All":
    filtered_df = filtered_df[filtered_df["category"] == category_filter]

st.write(f"Displaying **{len(filtered_df)} incidents** based on selected filters.")

# ---------------- CHARTS ----------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Incidents by Category")
    if not filtered_df.empty:
        st.bar_chart(filtered_df["category"].value_counts())
    else:
        st.info("No data to display.")

with col2:
    st.subheader("Incidents Over Time")
    if "timestamp" in filtered_df.columns and not filtered_df.empty:
        filtered_df["timestamp"] = pd.to_datetime(filtered_df["timestamp"], errors='coerce')
        incidents_over_time = filtered_df.groupby(filtered_df["timestamp"].dt.date).size()
        st.line_chart(incidents_over_time)
    else:
        st.info("No data to display.")

# ---------------- SUMMARY METRICS ----------------
st.subheader("Summary Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Incidents", len(filtered_df))
col2.metric("Open Incidents", len(filtered_df[filtered_df["status"] == "Open"]))
col3.metric("Closed/Resolved", len(filtered_df[filtered_df["status"].isin(["Closed", "Resolved"])]))

# ---------------- RAW DATA ----------------
with st.expander("See raw data"):
    st.dataframe(filtered_df)

# ---------------- LOGOUT ----------------
st.divider()
if st.button("Log Out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = None
    st.info("You have been logged out.")
    st.switch_page("home.py")
