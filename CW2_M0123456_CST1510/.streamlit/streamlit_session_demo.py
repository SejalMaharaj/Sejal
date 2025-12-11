import streamlit as st

st.title("Chat History with Session State")

# 1. Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Display all previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):  # "user" or "assistant"
        st.markdown(message["content"])

# 3. Get user input
prompt = st.chat_input("Say something...")

# 4. If the user submits a message
if prompt:

    # --- Save user message ---
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # --- Display user message immediately ---
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- Generate placeholder AI response (fake for now) ---
    ai_response = f"You said: {prompt}"

    # --- Save AI response ---
    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_response
    })

    # --- Display AI response ---
    with st.chat_message("assistant"):
        st.markdown(ai_response)
