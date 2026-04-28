import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load environment variables from .env file
load_dotenv()

# TODO 1: Initialize the InferenceClient
# Use model="mistralai/Mistral-7B-Instruct-v0.2:featherless-ai"
# Get your token using os.getenv("HF_TOKEN") and set `api_key`
client = ...

# TODO 2: Create a messages list.
# Give the bot a "system" role to define its personality.
# Give the "user" role a question to ask.
messages = [
    # {"role": "system", "content": "..."},
    # {"role": "user", "content": "... "}
]

print("Sending request to Hugging Face...")

# TODO 3: Call the chat_completion API
# Pass the messages list and set a max_tokens limit (e.g., 256)
response = ...

# TODO 4: Print the response content
print("\n--- AI Response ---")
# Hint: response.choices[0].message.content
print(...)
