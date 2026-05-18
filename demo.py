import gradio as gr

# Extra imports used in other phases, essential to import here to verify propoer env setup
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from langchain_community.document_loaders import CSVLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage



def greet(name):
    return "Hello " + name + "!"


demo = gr.Interface(fn=greet, inputs="text", outputs="text")
demo.launch()
