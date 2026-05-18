import os

from dotenv import load_dotenv
import gradio as gr
from langchain_community.document_loaders import CSVLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage


load_dotenv()


# Initialize the LangChain Hugging Face Model
llm = HuggingFaceEndpoint(
    model="mistralai/Mistral-7B-Instruct-v0.2:featherless-ai",
    task="text-generation",
    max_new_tokens=512,
    huggingfacehub_api_token=os.getenv("HF_TOKEN")
)
chat_model = ChatHuggingFace(llm=llm)


def process_file(files):
    all_documents = []

    # 1. Loop through all uploaded files and load them
    for file in files:
        if file.name.endswith('.csv'):
            loader = CSVLoader(file.name)
        elif file.name.endswith('.pdf'):
            loader = PyPDFLoader(file.name)
        else:
            continue  # Skip unsupported formats silently

        documents = loader.load()
        all_documents.extend(documents)

    if not all_documents:
        return gr.update(value="❌ No valid CSV or PDF files found.", visible=True)

    # 2. Chunk all documents together
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(all_documents)

    # 3. Embed and store in the Vector Database
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(chunks, embeddings)

    # We return the UI update AND the newly created vector store
    return gr.update(value=f"✅ Database Ready! Processed {len(chunks)} chunks from {len(files)} files.", visible=True), vector_store


def respond(message, history, system_prompt, vector_store):
    if vector_store is None:
        return "⚠️ Please upload a CSV or PDF file first!"

    # 1. Safely extract the current message string
    # Gradio might pass 'message' as a string, a dict, or a list of dicts.
    user_text = ""
    if isinstance(message, str):
        user_text = message
    elif isinstance(message, dict) and "text" in message:
        user_text = message["text"]
    elif isinstance(message, list):
        for item in message:
            if isinstance(item, dict) and item.get("type") == "text":
                user_text += item.get("text", "")

    # Retrieve top 3 most relevant chunks from FAISS
    relevant_docs = vector_store.similarity_search(user_text, k=3)
    context = "\n".join([doc.page_content for doc in relevant_docs])

    messages = []

    # Combine the user's dynamic System Prompt with the strict RAG instructions
    full_system_prompt = (
        f"{system_prompt}\n\n"
        "Use ONLY the following context to answer the user's question. "
        "If the answer is not in the context, politely say you do not know.\n\n"
        f"CONTEXT:\n{context}"
    )
    messages.append(SystemMessage(content=full_system_prompt))

    # 2. Reconstruct history by parsing the list of dicts
    for msg in history:
        role = msg.get("role")
        raw_content = msg.get("content")

        # Extract text from the content payload
        text_content = ""
        if isinstance(raw_content, str):
            text_content = raw_content
        elif isinstance(raw_content, list):
            for item in raw_content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text_content += item.get("text", "")

        # Map to LangChain message objects
        if role == "user":
            messages.append(HumanMessage(content=text_content))
        elif role == "assistant":
            messages.append(AIMessage(content=text_content))

    # Append the current extracted user message
    messages.append(HumanMessage(content=user_text))

    # Invoke the LangChain model
    response = chat_model.invoke(messages)
    return response.content


# --- UI SETUP ---
with gr.Blocks() as demo:
    # Change 3: Define a session-specific state variable to hold the vector store
    session_vector_store = gr.State(value=None)

    gr.Markdown("# 🏢 Enterprise AI Support Bot")
    gr.Markdown("Upload a document (CSV or PDF) to inject knowledge, and customize the bot's persona on the fly!")

    with gr.Row():
        file_upload = gr.File(
            label="Upload Document (.csv or .pdf)",
            file_types=[".csv", ".pdf"],
            file_count="multiple",
        )
        status_text = gr.Markdown("Waiting for file upload...", visible=False)

    chatbot = gr.ChatInterface(
        fn=respond,
        # This adds an expandable accordion at the bottom of the chat UI
        additional_inputs=[
            gr.Textbox(
                value="You are an expert, friendly customer support agent.",
                label="System Prompt (Define the Bot's Persona & Rules)",
                # lines=2
            ),
            session_vector_store # Inject the state into the respond function
        ]
    )

    # Wire the upload button to update BOTH the status text and the session state
    file_upload.upload(
        fn=process_file,
        inputs=file_upload,
        outputs=[status_text, session_vector_store]
    )


if __name__ == "__main__":
    demo.launch()
