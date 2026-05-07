import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.2:featherless-ai",
    api_key=os.getenv("HF_TOKEN")
)

messages = [
    {"role": "system", "content": "You are a helpful, concise AI assistant."},
    {"role": "user", "content": "Explain what a Large Language Model is in one sentence."}
]

print("Sending request to Hugging Face...")

response = client.chat_completion(
    messages=messages,
    max_tokens=256
)


print("\n--- AI Response ---")
print(response.choices[0].message.content)
