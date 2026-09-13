
import os

import streamlit as st
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

from langchain_community.document_loaders import (
    DirectoryLoader,
    Docx2txtLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# ============================================================
# Configuration
# ============================================================

# Load environment variables from .env
load_dotenv()

# Get Hugging Face API token
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

if not HUGGINGFACEHUB_API_TOKEN:
    raise ValueError(
        "HUGGINGFACEHUB_API_TOKEN is not set. "
        "Please add it to your .env file."
    )


# Hugging Face model
MODEL_NAME = "google/gemma-2-2b-it"


# ============================================================
# Step 1: Load documents
# ============================================================

def load_documents():
    """Load all DOCX files from the documents folder."""

    loader = DirectoryLoader(
        "./documents/",
        glob="**/*.docx",
        loader_cls=Docx2txtLoader,
    )

    return loader.load()


# ============================================================
# Step 2: Split documents into chunks
# ============================================================

def split_documents(documents):
    """Split documents into smaller chunks for retrieval."""

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    return text_splitter.split_documents(documents)


# ============================================================
# Step 3: Create vector store
# ============================================================

def create_vector_store(texts):
    """Create embeddings and store them in Chroma."""

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )

    vector_store = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory="./chroma_db",
    )

    return vector_store


# ============================================================
# Step 4: Create retriever
# ============================================================

def setup_retriever(vector_store):
    """Create a retriever from the vector store."""

    return vector_store.as_retriever(
        search_kwargs={"k": 3}
    )


# ============================================================
# Step 5: Generate answer using Hugging Face
# ============================================================

def query_ai(retriever, user_query):
    """Retrieve relevant documents and generate an answer."""

    # Retrieve relevant document chunks
    documents = retriever.invoke(user_query)

    # Check whether anything was retrieved
    if not documents:
        return "I could not find relevant information in the provided documents."

    # Combine retrieved chunks into context
    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    # Create prompt
    prompt = f"""
You are a helpful assistant that answers questions based only on
the provided documents.

Use the context below to answer the user's question.

If the answer cannot be found in the context, say:
"I could not find the answer in the provided documents."

Do not make up information.

Context:
--------------------
{context}
--------------------

Question:
{user_query}

Answer:
"""

    # Create Hugging Face client
    client = InferenceClient(
        api_key=HUGGINGFACEHUB_API_TOKEN,
        provider="auto",
    )

    # Send request to Hugging Face
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        max_tokens=512,
        temperature=0.5,
    )

    # Extract generated answer
    return response.choices[0].message.content


# ============================================================
# Step 6: Main Streamlit application
# ============================================================

def main():

    st.title("🤖 Custom AI Chatbot")
    st.write("Ask questions based on your documents!")

    # --------------------------------------------------------
    # Load and process documents
    # --------------------------------------------------------

    if "retriever" not in st.session_state:

        with st.spinner(
            "Loading and processing your documents..."
        ):

            try:

                documents = load_documents()

                if not documents:
                    st.error(
                        "No .docx files found in the "
                        "./documents/ folder."
                    )
                    return

                # Split documents
                texts = split_documents(documents)

                # Create vector store
                vector_store = create_vector_store(texts)

                # Create retriever
                retriever = setup_retriever(vector_store)

                # Store objects in Streamlit session
                st.session_state.vector_store = vector_store
                st.session_state.retriever = retriever

                st.success(
                    "Documents loaded! Ready to chat."
                )

            except Exception as error:

                st.error(
                    f"Error loading documents: "
                    f"{type(error).__name__}: {error}"
                )

                st.exception(error)

                return

    # --------------------------------------------------------
    # Chat interface
    # --------------------------------------------------------

    user_query = st.text_input(
        "Ask a question:"
    )

    if user_query:

        with st.spinner("Thinking..."):

            try:

                answer = query_ai(
                    st.session_state.retriever,
                    user_query,
                )

                st.write("**Answer:**")
                st.write(answer)

            except Exception as error:

                st.error(
                    f"Error generating answer: "
                    f"{type(error).__name__}: {error}"
                )

                st.exception(error)


# ============================================================
# Application entry point
# ============================================================

if __name__ == "__main__":
    main()
