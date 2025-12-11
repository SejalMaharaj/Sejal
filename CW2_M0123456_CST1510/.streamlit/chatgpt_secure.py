import google.generativeai as genai
from dotenv import load_dotenv
import os

#Load API Key from .env file

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("API key not found. Make sure GOOGLE_API_KEY is in your .env file.")

#Configure Gemini
genai.configure(api_key=api_key)


#Initialize model

model = genai.GenerativeModel("gemini-2.5-flash")


# Conversation history

messages = [
    {
        "role": "user",
        "parts": [{"text": "You are a helpful assistant."}]
    }
]

print("Gemini Console Chat (type 'quit' to exit)")
print("-" * 50)


# Chat Loop

while True:
    user_input = input("You: ")

    if user_input.lower() == "quit":
        print("Goodbye!")
        break

    # Add user message
    messages.append({
        "role": "user",
        "parts": [{"text": user_input}]
    })

    # Send entire conversation to Gemini
    response = model.generate_content(messages)

    assistant_message = response.text

    # Add model response
    messages.append({
        "role": "model",
        "parts": [{"text": assistant_message}]
    })

    print(f"AI: {assistant_message}\n")

