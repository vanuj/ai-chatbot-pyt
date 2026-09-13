# ai-chatbot-pyt
Simple AI chatbot in python to quickly interact with the uploaded document and retrieve answers.
# AI RAG Chatbot

A simple local **RAG (Retrieval-Augmented Generation) chatbot** built with Streamlit, LangChain, Chroma, Hugging Face embeddings, and Gemma.

The chatbot can:

* Chat with your documents using natural language.
* Maintain conversation history.
* Show the documents used to generate an answer.
* Upload multiple DOCX documents.
* Add and remove documents from the knowledge base.

## Project Structure

```text
ai-chatbot-pyt/
├── app.py
├── .env
├── documents/
├── chroma_db/
└── README.md
```

## Prerequisites

Install **Python 3.9+**.

You also need a Hugging Face API token.

Create one from:
https://huggingface.co/settings/tokens

---

## macOS Setup

### 1. Install Python

Using Homebrew:

```bash
brew install python
```

Verify:

```bash
python3 --version
```

### 2. Clone/Open the project

```bash
cd /path/to/ai-chatbot-pyt
```

### 3. Create a virtual environment

```bash
python3 -m venv .venv
```

### 4. Activate the environment

```bash
source .venv/bin/activate
```

You should see:

```text
(.venv)
```

in your terminal.

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` does not exist yet:

```bash
pip install streamlit python-dotenv huggingface-hub \
langchain langchain-community langchain-huggingface \
langchain-chroma chromadb docx2txt \
sentence-transformers
```

---

## Windows Setup

### 1. Install Python

Download Python from:

https://www.python.org/downloads/

During installation, make sure to select:

```text
Add Python to PATH
```

Verify:

```cmd
python --version
```

### 2. Open the project

```cmd
cd path\to\ai-chatbot-pyt
```

### 3. Create a virtual environment

```cmd
python -m venv .venv
```

### 4. Activate the environment

Command Prompt:

```cmd
.venv\Scripts\activate
```

PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```cmd
pip install -r requirements.txt
```

Or, if `requirements.txt` does not exist:

```cmd
pip install streamlit python-dotenv huggingface-hub langchain langchain-community langchain-huggingface langchain-chroma chromadb docx2txt sentence-transformers
```

---

## Configure Hugging Face

Create a `.env` file in the project root:

```env
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token
```

Example:

```text
ai-chatbot-pyt/
├── app.py
├── .env
├── documents/
└── chroma_db/
```

Do not commit `.env` to Git.

Add this to `.gitignore`:

```gitignore
.env
.venv/
chroma_db/
__pycache__/
```

---

## Add Documents

Place your initial DOCX files inside:

```text
documents/
```

For example:

```text
documents/
├── employee_handbook.docx
├── leave_policy.docx
└── project_guidelines.docx
```

You can also upload multiple DOCX files directly from the Streamlit UI.

---

## Run the Application

Make sure the virtual environment is activated.

### macOS

```bash
streamlit run app.py
```

### Windows

```cmd
streamlit run app.py
```

Streamlit will provide a local URL, usually:

```text
http://localhost:8501
```

Open it in your browser.

---

## First Run

On the first run, the application will:

1. Load documents from `documents/`.
2. Split them into smaller chunks.
3. Generate embeddings.
4. Create the Chroma vector database.
5. Start the chatbot.

The generated vector database is stored in:

```text
chroma_db/
```

You normally don't need to modify this directory manually.

---

## Useful Commands

Activate environment:

**macOS**

```bash
source .venv/bin/activate
```

**Windows**

```cmd
.venv\Scripts\activate
```

Run application:

```bash
streamlit run app.py
```

Stop application:

```text
Ctrl + C
```

Deactivate environment:

```bash
deactivate
```

Update pip:

```bash
python -m pip install --upgrade pip
```

---

## Tech Stack

* Python
* Streamlit
* LangChain
* Chroma
* Hugging Face
* Gemma 2B
* Sentence Transformers
* DOCX / Docx2txt

## Notes

This is a local development project. The application uses Hugging Face for the LLM inference and runs the document processing and vector database locally.

For production use, authentication, persistent storage, document lifecycle management, monitoring, and evaluation should be added.
