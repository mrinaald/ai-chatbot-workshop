import gradio as gr
from huggingface_hub import InferenceClient


def greet(name):
    return "Hello " + name + "!"


demo = gr.Interface(fn=greet, inputs="text", outputs="text")
demo.launch()
