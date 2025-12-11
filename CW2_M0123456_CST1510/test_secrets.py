import streamlit as st

st.title("Test Secrets Setup - Gemini")

try:
    api_key = st.secrets["GOOGLE_GEMINI_API_KEY"]
    st.success("API key loaded successfully!")
    st.write(f"Key starts with: {api_key[:10]}...")
except Exception as e:
    st.error(f"Error loading API key: {e}")
    st.info("Make sure .streamlit/secrets.toml exists and contains GOOGLE_GEMINI_API_KEY")
