---
title: Enterprise AI Support Bot
emoji: 🏢
colorFrom: yellow
colorTo: red
sdk: gradio
sdk_version: 6.14.0
app_file: app.py
license: mit
python_version: 3.12.10
---

# 🏢 RAG AI Assistant

This Space hosts a Retrieval-Augmented Generation (RAG) chatbot that allows you to inject custom knowledge into an open-source Large Language Model. It is built using LangChain, FAISS, and Gradio.

## 🚀 How to Use

1. **Upload a Document:** Drag and drop a `.csv` or `.pdf` file into the upload box. The app will automatically chunk the text and embed it into a FAISS vector database. Wait for the "✅ Database Ready!" confirmation.
2. **Set the Persona:** Expand the "Additional Inputs" section at the bottom of the chat to customize the bot's System Prompt (e.g., "You are a pirate customer support agent").
3. **Chat:** Ask questions! The bot will retrieve relevant chunks from your document and use them to formulate its answer.

## 🛠️ Tech Stack

* **LLM:** Mistral-7B (via Hugging Face Inference API)
* **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2`
* **RAG Framework:** LangChain (PyPDFLoader, CSVLoader, FAISS)
* **Frontend:** Gradio
