import streamlit as st
import google.generativeai as genai


# Configure Gemini from secrets

api_key = st.secrets.get("GOOGLE_GEMINI_API_KEY")

if not api_key:
    st.error("GOOGLE_GEMINI_API_KEY not found in .streamlit/secrets.toml")
    st.stop()

CYBER_SYSTEM_PROMPT = """
You are a cybersecurity expert assistant.
- Analyze incidents and threats
- Provide technical guidance
- Explain attack vectors and mitigations
- Use standard terminology (MITRE ATT&CK, CVE)
- Prioritize actionable recommendations
Tone: Professional, technical
Format: Clear, structured responses.
"""

genai.configure(api_key=api_key)

# Create model with system instruction for domain behavior
model = genai.GenerativeModel(
    "gemini-2.5-flash",
    system_instruction=CYBER_SYSTEM_PROMPT
)


# Streamlit UI

st.title(" Sejal's Cybersecurity AI Assistant")

# Initialize session state for messages
# We store only user and assistant messages here
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
prompt = st.chat_input("Ask about cybersecurity...")

if prompt:
    # Display user message in the chat
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add user message to session state
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Build Gemini formatted messages from history
    gemini_messages = []
    for m in st.session_state.messages:
        role = "user" if m["role"] == "user" else "model"
        gemini_messages.append({
            "role": role,
            "parts": [{"text": m["content"]}]
        })

    # Call Gemini model
    try:
        response = model.generate_content(gemini_messages)
        assistant_text = response.text
    except Exception as e:
        assistant_text = f"Error calling Gemini API: {e}"

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(assistant_text)

    # Add assistant response to session state
    st.session_state.messages.append({
        "role": "assistant",
        "content": assistant_text
    })
