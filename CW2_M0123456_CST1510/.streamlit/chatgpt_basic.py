import google.generativeai as genai

# --- SETUP ---
genai.configure(api_key="AIzaSyDO6OinSKMhrr8GYt3MKOzY0VqYeU6czhw")

# Select a supported model
model = genai.GenerativeModel("gemini-2.5-flash")  # Choose a valid model

# Initialize conversation with the first "user" message containing instructions
messages = [
    {"role": "user", "parts": [{"text": "You are a helpful assistant."}]}
]

print("Google Gemini Console Chat (type 'quit' to exit)")
print("-" * 50)

while True:
    # Get user input
    user_input = input("You: ")

    if user_input.lower() == "quit":
        print("Goodbye!")
        break

    # Add user input to messages
    messages.append({"role": "user", "parts": [{"text": user_input}]})

    # Generate response from the model
    response = model.generate_content(messages)

    # Extract the assistant text
    assistant_message = response.text

    # Add the assistant response as "model" role
    messages.append({"role": "model", "parts": [{"text": assistant_message}]})

    # Display response
    print(f"AI: {assistant_message}\n")
