import streamlit as st

st.title("Test Google Gemini API Key Setup")

try:
    # Access your API key from Streamlit secrets
    api_key = st.secrets["GOOGLE_GEMINI_API_KEY"]
    st.success("Google Gemini API key loaded successfully!")
    st.write(f"Key starts with: {api_key[:10]}...")
except Exception as e:
    st.error(f"Error loading API key: {e}")
    st.info("Make sure .streamlit/secrets.toml exists and contains GOOGLE_GEMINI_API_KEY")
