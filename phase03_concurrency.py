import os
import gradio as gr
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

SYSTEM_PROMPT ="""You are a helpful, concise, and friendly AI assistant.

Your goals:
- Provide clear, accurate, and relevant answers.
- Maintain natural, conversational tone across multiple turns.
- Ask follow-up questions when useful to clarify user intent.
- Remember context from earlier in the conversation and use it when appropriate.

Guidelines:
- Be concise but not abrupt; expand only when helpful.
- If the user's request is unclear, ask a brief clarifying question.
- Avoid repeating information unnecessarily.
- If you don't know something, say so honestly instead of guessing.
- Break down complex topics into simple explanations.

Behavior:
- Adapt to the user's style (casual, formal, technical).
- Prefer practical, actionable responses.
- Stay on topic and avoid unnecessary tangents.
"""


client = InferenceClient(
    # model="HuggingFaceH4/zephyr-7b-beta:featherless-ai",
    model="mistralai/Mistral-7B-Instruct-v0.2:featherless-ai",
    api_key=os.getenv("HF_TOKEN")
)

async def respond(message, history):
    formatted_messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for msg in history:
        formatted_messages.append(msg)

    formatted_messages.append({"role": "user", "content": message})

    response = client.chat_completion(
        messages=formatted_messages,
        max_tokens=256
    )
    return response.choices[0].message.content

demo = gr.ChatInterface(
    fn=respond,
    title="Concurrent AI Assistant",
    # save_history=True,
    multimodal=True,
)

# Instructor Note:
# 1. Gradio inherently manages session state per browser tab (preventing history mixing).
# 2. .queue() acts as a traffic controller.
# default_concurrency_limit=2 means it will process 2 messages simultaneously.
# The 3rd person will see a "You are in queue" message instead of crashing the app.
# demo.queue(default_concurrency_limit=2)
# max_size=1 means only 1 person can be in the queue.
# If 1 person is chatting and another tries to, they get a "full" message.
demo.queue(
    default_concurrency_limit=1,
    max_size=1
)


if __name__ == "__main__":
    demo.launch()
