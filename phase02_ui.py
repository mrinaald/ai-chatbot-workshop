import os
import gradio as gr
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.2:featherless-ai",
    api_key=os.getenv("HF_TOKEN")
)

SYSTEM_PROMPT = "You are a friendly AI."


def respond(message, history):
    # 'history' is a list of dicts: [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
    # The API needs a list of dictionaries: [{"role": "...", "content": "..."}, ...]

    formatted_messages = []

    # TODO 1: Add a system prompt to the beginning of formatted_messages

    # TODO 2: Loop through the 'history' and append both the user and assistant messages
    # for msg in history:
    #     ... append msg dict ...

    # TODO 3: Append the current user 'message'

    # TODO 4: Call the API and return the text response
    response = ...

    return response.choices[0].message.content


# TODO 5: Create a gr.ChatInterface using your respond function and launch it
demo = gr.ChatInterface(
    ...
)


if __name__ == "__main__":
    # TODO 6: Launch the app
    pass
