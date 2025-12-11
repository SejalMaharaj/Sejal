# 3_DataScience.py
import streamlit as st
import pandas as pd
from db import connect_database

st.set_page_config(page_title="Data Science Dashboard", page_icon="📈", layout="wide")

# ---------------- SESSION CHECK ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = None

# Guard: only accessible to logged-in Data Science users
if not st.session_state.logged_in or st.session_state.role != "datascience":
    st.error("You must be logged in as a Data Science user to view this page.")
    if st.button("Go to Login Page"):
        st.switch_page("home.py")
    st.stop()

# ---------------- DASHBOARD ----------------
st.title("📈 Data Science Dashboard")
st.success(f"Hello, **{st.session_state.username}**! You are logged in as Data Science.")

# ---------------- DATABASE ----------------
conn = connect_database()
datasets_df = pd.read_sql("SELECT * FROM datasets", conn)
conn.close()

# ---------------- INLINE FILTERS ----------------
st.subheader("Filter Datasets")
col1, col2 = st.columns(2)

with col1:
    name_filter = st.selectbox(
        "Select Dataset Name",
        options=["All"] + list(datasets_df["name"].unique())
    )

with col2:
    uploader_filter = st.selectbox(
        "Select Uploaded By",
        options=["All"] + list(datasets_df["uploaded_by"].unique())
    )

# Apply filters
filtered_df = datasets_df.copy()
if name_filter != "All":
    filtered_df = filtered_df[filtered_df["name"] == name_filter]

if uploader_filter != "All":
    filtered_df = filtered_df[filtered_df["uploaded_by"] == uploader_filter]

st.write(f"Displaying **{len(filtered_df)} datasets** based on selected filters.")

# ---------------- CHARTS ----------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Number of Columns per Dataset")
    if "columns" in filtered_df.columns and not filtered_df.empty:
        st.bar_chart(filtered_df["columns"].value_counts())
    else:
        st.info("Column 'columns' not found or no data to display.")

with col2:
    st.subheader("Rows per Dataset")
    if "rows" in filtered_df.columns and not filtered_df.empty:
        st.line_chart(filtered_df["rows"])
    else:
        st.info("Column 'rows' not found or no data to display.")

# ---------------- SUMMARY METRICS ----------------
st.subheader("Summary Metrics")
col1, col2 = st.columns(2)
col1.metric("Total Datasets", len(filtered_df))
if "rows" in filtered_df.columns:
    col2.metric("Total Rows Across Datasets", filtered_df["rows"].sum())

# ---------------- RAW DATA ----------------
with st.expander("See raw dataset information"):
    st.dataframe(filtered_df)

# ---------------- LOGOUT ----------------
st.divider()
if st.button("Log Out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = None
    st.info("You have been logged out.")
    st.switch_page("home.py")

import streamlit as st

st.title("Questions?")

if st.button("Open AI Assistant"):
    st.switch_page("pages/AI_assistant.py")
