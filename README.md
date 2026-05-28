# 🚀 Build an End-to-End AI Chatbot Assistant in 60 Minutes

Welcome to the AI Chatbot Assistant Workshop! In this 1-hour session, we will build a conversational AI chatbot from scratch, run it locally on your machine, and deploy it live to the public internet.

We will be using **Hugging Face's free Inference API** for the AI model and **Gradio** for the web interface.

---

## 🛠️ Pre-Workshop Setup

Before we begin, please ensure your local environment is ready so we can jump straight into coding.

1. **Create a Hugging Face Account:** Sign up for free at [huggingface.co](https://huggingface.co/).
2. **Generate an API Token:**
   * Go to your Hugging Face Settings > Access Tokens.
   * Create a new token with **Write** or **Fine-grained** permissions. Copy this token; you will need it later.
3. **Clone this Repository:**
   ```bash
   git clone https://github.com/mrinaald/ai-chatbot-workshop
   cd ai-chatbot-workshop
   ```
4. **Set Up Your Environment:**
   Make sure you have Python 3.11+ installed. Create a python environment and activate it. Then, install the required packages in your virtual environment:
   ```bash
   pip install -r requirements.txt
   ```
5. **Create your Secrets File:**
   Create a new file named `.env` in the root folder of this project and add your token. The file should look like:
   ```env
   HF_TOKEN=your_hugging_face_token
   ```
   where `your_hugging_face_token` is the actual value of the token you copied from HuggingFace.

---

## 📝 Workshop Phases & Code Snippets

During the workshop, you will work inside the `student/` folder. Open the files and look for the `# TODO` comments.

### Phase 1: Basic Chatbot API Call
**File:** `student/phase01_basic.py`
**Goal:** Make our first successful call to the Hugging Face API using a static prompt.

**Code to fill in:**
```python
# TODO 1: Initialize the InferenceClient
client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.2:featherless-ai",
    api_key=os.getenv("HF_TOKEN")
)

# TODO 2: Create a messages list.
messages = [
    {"role": "system", "content": "You are a helpful and concise AI assistant."},
    {"role": "user", "content": "Explain what an AI agent is in one sentence."}
]

# TODO 3: Call the chat_completion API
response = client.chat_completion(
    messages=messages,
    max_tokens=256
)

# TODO 4: Print the response content
print(response.choices[0].message.content)
```
**Run it:** `python student/phase01_basic.py`

---

### Phase 2: Full Local Chatbot (UI & Memory)
**File:** `student/phase02_ui.py`
**Goal:** Wrap our AI in a web interface and give it "memory" so it remembers the conversation history.

**Code to fill in:**
```python
    # TODO 1: Add a system prompt to the beginning of formatted_messages
    formatted_messages.append({"role": "system", "content": SYSTEM_PROMPT})

    # TODO 2: Loop through the 'history' and append both the user and assistant messages
    for msg in history:
        formatted_messages.append(msg)

    # TODO 3: Append the current user 'message'
    formatted_messages.append({"role": "user", "content": message})

    # TODO 4: Call the API and return the text response
    response = client.chat_completion(messages=formatted_messages, max_tokens=512)

# ... further down the file ...

# TODO 5: Create a gr.ChatInterface using your respond function and launch it
demo = gr.ChatInterface(
    fn=respond,
    title="My Local AI Assistant",
    description="Powered by Hugging Face and Gradio"
)

# TODO 6: Launch the app
demo.launch()
```
**Run it:** `python student/phase02_ui.py` (Then click the `http://127.0.0.1:7860` link in your terminal!)

---

### Phase 3: RAG Pipeline
**File:** `student/phase03_rag.py`
**Goal:** Learn how to implement a local Retrieval Augmented Generation (RAG) pipeline using LangChain.

**Code to fill in:**
```python
# TODO 1: Chunk the documents
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents(documents)

# TODO 2: Initialize the Vector Database
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_store = FAISS.from_documents(chunks, embeddings)


# TODO 3: Retrieve the relevant documents
relevant_docs = vector_store.similarity_search(user_text, k=3)
context = "\n".join([doc.page_content for doc in relevant_docs])

# TODO 4: Create the final System Prompt
full_system_prompt = (
    f"{system_prompt}\n\n"
    f"CONTEXT:\n{context}"
)
```
**Run it:** `python student/phase03_rag.py`

---

### Phase 4: Deploying to the Public Web (Hugging Face Spaces)
**Goal:** Move your local code to a cloud server so anyone in the world can use your chatbot.

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces) and click **Create new Space**.
2. **Name:** `my-first-ai-chatbot` (or similar).
3. **SDK:** Select **Gradio**.
4. **Hardware:** Free (CPU basic). Click **Create Space**.
5. **Secure your API Key (CRITICAL):**
   * Go to your Space's **Settings** tab.
   * Scroll down to **Variables and secrets**.
   * Click **New secret**. Name it `HF_TOKEN` and paste your actual token as the value.
6. **Upload your code:**
   * Go to the **Files** tab in your Space.
   * Click **Add file > Upload files**.
   * Upload `requirements.txt`, `phase03_rag.py`, and `README_hf.md` from your local folder.
     + *Important:* Rename `phase03_rag.py` to `app.py` in the browser interface.
     + *Important:* Rename `README_hf.md` to `README.md` in the browser interface.
   * Commit the changes! Wait 10-15 minutes for the app to Build, and share your link!


## Extra
We can use a very sophisticated system prompt as well to make the chatbot more robust.

For instance, in the `phase02_ui.py`, we can use the following system prompt:
```python
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
```

Similarly for `phase03_rag.py`, we can use something like this:
```python
SYSTEM_PROMPT = """You are a professional, accurate, and helpful enterprise AI assistant.

Your primary objective is to answer the user's questions based EXCLUSIVELY on the provided CONTEXT.

CRITICAL INSTRUCTIONS:
1. Grounding: You must rely STRICTLY on the retrieved CONTEXT to formulate your answer. Do not use outside knowledge.
2. Missing Information: If the CONTEXT does not contain the exact answer to the user's query, you must state: "I'm sorry but I don't have the information you need. Please allow me to connect you with a human operator." Do NOT guess, infer, or hallucinate details.
3. Tone: Maintain a polite, objective, and concise tone.
4. Formatting: Use bullet points for lists and keep paragraphs short for readability.
5. Casual Chat: If the user says hello or asks a casual greeting, respond politely and ask how you can help them with their documents today.
"""
```

