# my_app/pages/AI_assistant.py

import streamlit as st
from app.services.ai_assistant import DomainAssistant, DomainAssistantConfig

# Load API key
api_key = st.secrets.get("GOOGLE_GEMINI_API_KEY")
if not api_key:
    st.error("No GOOGLE_GEMINI_API_KEY found in .streamlit/secrets.toml")
    st.stop()

# Domain-specific prompts (same as before)
DOMAIN_PROMPTS = {
    "Cybersecurity": """
You are a cybersecurity expert assistant.
Analyse incidents and threats. Explain attack vectors, MITRE ATT&CK mapping, CVEs,
and provide actionable mitigation steps.
""",
    "Data Science": """
You are a data science expert assistant.
Help with statistical analysis, visualisation, modelling, and interpreting datasets clearly.
""",
    "IT Operations": """
You are an IT operations expert assistant.
Troubleshoot outages, performance issues, networking problems, and ticket resolutions.
"""
}

# Available models
AVAILABLE_MODELS = [
    "gemini-2.5-flash",
    "gemini-flash-lite-latest"
]

# Create assistant service (OOP)
config = DomainAssistantConfig(system_prompts=DOMAIN_PROMPTS)
assistant = DomainAssistant(api_key=api_key, config=config)

# Page configuration
st.set_page_config(page_title="AI Assistant", page_icon="💬", layout="wide")

st.title("💬 Multi Domain AI Assistant")
st.caption("Powered by Google Gemini")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar controls
with st.sidebar:
    st.subheader("Assistant Settings")

    domain = st.selectbox(
        "Choose Domain",
        ["Cybersecurity", "Data Science", "IT Operations"]
    )

    model_name = st.selectbox("Model", AVAILABLE_MODELS, index=0)

    temperature = st.slider(
        "Creativity (Temperature)",
        min_value=0.0,
        max_value=2.0,
        value=1.0,
        step=0.1
    )

    if st.button("Clear Chat 🗑", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
prompt = st.chat_input(f"Ask something related to {domain}...")

if prompt:
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Call our OOP assistant to stream a reply
    stream = assistant.stream_reply(
        domain=domain,
        history=st.session_state.messages,
        model_name=model_name,
        temperature=temperature,
    )

    # Display streaming response
    with st.chat_message("assistant"):
        container = st.empty()
        full_reply = ""

        try:
            for chunk in stream:
                piece = ""
                for candidate in chunk.candidates:
                    for part in candidate.content.parts:
                        if hasattr(part, "text") and part.text:
                            piece += part.text

                if piece:
                    full_reply += piece
                    container.markdown(full_reply + "▌")

            container.markdown(full_reply)

        except Exception as e:
            full_reply = f"Error generating response: {e}"
            container.markdown(full_reply)

    # Save assistant reply
    st.session_state.messages.append({
        "role": "assistant",
        "content": full_reply
    })
