import streamlit as st
import pandas as pd

st.title("First page")
st.subheader("This is a subheader")

# --------------------------------------
# NAME INPUT
# --------------------------------------
name = st.text_input("Enter your name")
if st.button("Submit"):
    st.subheader(f"Hello, {name}")

df = pd.DataFrame({
    "User": ["Alice", "Bob", "Charlie"],
    "Score": [52, 60, 88]
})

st.dataframe(df)


def get_all_incidents():
    return pd.DataFrame({
        "date": ["2025-01-01", "2025-01-02", "2025-01-03"],
        "severity": ["High", "Low", "Medium"],
        "type": ["Malware", "Phishing", "DDoS"],
        "status": ["Open", "Closed", "In Progress"]
    })

df_incidents = get_all_incidents()
st.subheader("Cyber Incidents")
st.dataframe(df_incidents)

#
col1, col2 = st.columns(2)
with col1:
    st.metric("High Severity", df_incidents[df_incidents["severity"] == "High"].shape[0])

with col2:
    st.metric("Total Incidents", df_incidents["severity"].count(), "+1")


severity_counts = df_incidents["severity"].value_counts().reset_index()
severity_counts.columns = ["severity", "count"]

st.bar_chart(severity_counts.set_index("severity"))

# --------------------------------------
# ADD INCIDENT FORM
# --------------------------------------
st.markdown("## Add Incidents ##")

with st.form("Add new incident"):
    date = st.date_input("Enter a date")
    incident_type = st.selectbox("Incident type", ["Malware", "Phishing", "DDoS"])
    severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
    status = st.selectbox("Status", ["Open", "Closed", "In Progress", "Resolved"])
    description = st.text_input("Description")
    submitted = st.form_submit_button("Submit")

if submitted:
    # Replace with your actual database insert function
    # insert_incident(date, incident_type, severity, status, description)
    st.success("Incident added!")
