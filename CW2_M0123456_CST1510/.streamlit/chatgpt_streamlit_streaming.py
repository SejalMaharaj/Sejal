import streamlit as st
import google.generativeai as genai


api_key = st.secrets.get("GOOGLE_GEMINI_API_KEY")

if not api_key:
    st.error("GOOGLE_GEMINI_API_KEY not found in .streamlit/secrets.toml")
    st.stop()

genai.configure(api_key=api_key)

# Available Gemini models for the dropdown
AVAILABLE_MODELS = [
    "gemini-2.5-flash",
    "gemini-flash-lite-latest",
]


# Page configuration

st.set_page_config(
    page_title="Chat Assistant",
    page_icon="💬",
    layout="wide"
)

# Title
st.title("Sejal's Gemini Chat Assistant")
st.caption("Powered by Google Gemini")


# Initialize session state

if "messages" not in st.session_state:
    # Store only user and assistant messages
    st.session_state.messages = []


# Sidebar controls

with st.sidebar:
    st.subheader("Chat Controls")

    # Message count
    message_count = len(st.session_state.messages)
    st.metric("Messages", message_count)

    # Clear chat button
    if st.button("🗑 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    # Model selection
    model_name = st.selectbox(
        "Model",
        AVAILABLE_MODELS,
        index=0
    )

    # Temperature slider
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=1.0,
        step=0.1,
        help="Higher values make output more random"
    )


# Display previous messages

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Get user input

prompt = st.chat_input("Say something...")

if prompt:
    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Build Gemini messages from history
    gemini_messages = []
    for m in st.session_state.messages:
        role = "user" if m["role"] == "user" else "model"
        gemini_messages.append({
            "role": role,
            "parts": [{"text": m["content"]}]
        })

    # Call Gemini with streaming
    with st.spinner("Thinking..."):
        model = genai.GenerativeModel(
            model_name,
            generation_config={
                "temperature": temperature
            }
        )


        # Streaming response

        with st.chat_message("assistant"):
            container = st.empty()
            full_reply = ""

            try:
                for chunk in model.generate_content(
                    gemini_messages,
                    stream=True
                ):
                    piece = ""

                    # Collect any text in this chunk
                    for candidate in chunk.candidates:
                        for part in candidate.content.parts:
                            if hasattr(part, "text") and part.text:
                                piece += part.text

                    if piece:
                        full_reply += piece
                        # Cursor effect at the end
                        container.markdown(full_reply + "▌")

                # Final reply without cursor
                container.markdown(full_reply)

            except Exception as e:
                full_reply = f"Error during streaming from Gemini API: {e}"
                container.markdown(full_reply)

    # Save assistant message to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": full_reply
    })
