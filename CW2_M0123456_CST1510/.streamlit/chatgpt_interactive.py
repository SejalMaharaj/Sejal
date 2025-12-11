import streamlit as st
import google.generativeai as genai

# -----------------------------
# Google Gemini setup
# -----------------------------
genai.configure(api_key="AIzaSyDO6OinSKMhrr8GYt3MKOzY0VqYeU6czhw")  # Replace with your API key
model = genai.GenerativeModel("gemini-2.5-flash")

# -----------------------------
# Streamlit page setup
# -----------------------------
st.title("Google Gemini Chat Demo - Part 2")

# -----------------------------
# 2.4 / 2.6: Initialize session state for messages
# -----------------------------
if 'messages' not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Display all previous messages
# -----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# 2.2: Get new user input
# -----------------------------
prompt = st.chat_input("Type your message here...")

if prompt:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display immediately
    with st.chat_message("user"):
        st.markdown(prompt)

    # -----------------------------
    # Simulate AI response (replace with Gemini API call)
    # -----------------------------
    # Prepare messages in Gemini format
    messages_for_ai = [
        {"role": "user", "parts": [{"text": msg["content"]}]}
        for msg in st.session_state.messages if msg["role"] == "user"
    ]

    # Call Gemini AI
    response = model.generate_content(messages_for_ai)
    ai_response = response.text

    # Save AI response
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

    # Display AI response
    with st.chat_message("assistant"):
        st.markdown(ai_response)

# -----------------------------
# Optional: Reset conversation button
# -----------------------------
if st.button("Reset Chat"):
    st.session_state.messages = []
    st.experimental_rerun()
