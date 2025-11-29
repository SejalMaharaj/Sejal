import streamlit as st
import pandas as pd
import plotly.express as px
from db import connect_database

st.set_page_config(page_title="IT Operations", page_icon="🛠️", layout="wide")

# ---------- AUTH CHECK ----------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to access this page.")
    st.stop()

username = st.session_state.get("username", "User")

st.title("🛠️ IT Operations Dashboard")
st.write(f"Hello, **{username}**! You are logged in as **IT Operations**.")

# ---------- LOAD IT DATA ----------
conn = connect_database()
tickets_df = pd.read_sql("SELECT * FROM it_tickets", conn)
conn.close()

# 🔥 FIX: Make dates Plotly-safe (string → datetime → safe format)
tickets_df["created_at"] = pd.to_datetime(tickets_df["created_at"], errors="coerce")

# ---------- FILTERS ----------
st.subheader("🎛 Filter IT Tickets")

col1, col2, col3 = st.columns(3)

priority_filter = col1.selectbox(
    "Filter by Priority",
    options=["All"] + sorted(tickets_df["priority"].unique())
)

status_filter = col2.selectbox(
    "Filter by Status",
    options=["All"] + sorted(tickets_df["status"].unique())
)

assigned_filter = col3.selectbox(
    "Filter by Assigned Staff",
    options=["All"] + sorted(tickets_df["assigned_to"].unique())
)

# Apply filters
filtered_df = tickets_df.copy()

if priority_filter != "All":
    filtered_df = filtered_df[filtered_df["priority"] == priority_filter]

if status_filter != "All":
    filtered_df = filtered_df[filtered_df["status"] == status_filter]

if assigned_filter != "All":
    filtered_df = filtered_df[filtered_df["assigned_to"] == assigned_filter]

# ---------- METRICS ----------
st.subheader("📌 Key Metrics")

m1, m2, m3 = st.columns(3)

m1.metric("Total Tickets", len(filtered_df))

avg_res = (
    round(filtered_df["resolution_time_hours"].mean(), 1)
    if not filtered_df.empty else 0
)
m2.metric("Avg Resolution Time (hrs)", avg_res)

open_tickets = sum(filtered_df["status"] != "Resolved")
m3.metric("Open Tickets", open_tickets)

# ---------- CHARTS ----------
st.subheader("📈 Ticket Trends & Patterns")

# Tickets by Priority
priority_counts = filtered_df.groupby("priority").size().reset_index(name="count")

fig_priority = px.bar(
    priority_counts,
    x="priority", y="count",
    title="Tickets by Priority",
)

# Tickets by Status
fig_status = px.pie(
    filtered_df,
    names="status",
    title="Ticket Status Breakdown"
)

# FIXED: Tickets Over Time (NO PeriodIndex)
temp_df = filtered_df.copy()
temp_df["month"] = temp_df["created_at"].dt.to_period("M").astype(str)

monthly_counts = temp_df.groupby("month").size().reset_index(name="count")

fig_time = px.line(
    monthly_counts,
    x="month",
    y="count",
    markers=True,
    title="Tickets Over Time (Monthly)"
)

# Display charts
c1, c2 = st.columns(2)
c1.plotly_chart(fig_priority, use_container_width=True)
c2.plotly_chart(fig_status, use_container_width=True)

st.plotly_chart(fig_time, use_container_width=True)

# ---------- RAW DATA ----------
st.subheader("📄 Filtered Ticket Records")
st.dataframe(filtered_df, use_container_width=True)

st.info("This dashboard helps IT Operations identify bottlenecks, slow staff, and urgent priorities.")
