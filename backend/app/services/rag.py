from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
import os

load_dotenv()

# Store the vector database in the chroma_db folder
CHROMA_PATH = "chroma_db"

# Embedding model — convert text to vectors
embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

def load_and_split(file_path: str):
    """
    Read the file and split it into small chunks
    chunk_size=500 — each chunk has at most 500 tokens
    chunk_overlap=50 — chunks overlap by 50 tokens to prevent semantic断裂
    """
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path)

    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)
    return chunks

def store_in_chroma(chunks):
    """
    Vectorize the text chunks and store them in ChromaDB
    If chroma_db already exists, it will automatically append new content
    """
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    return db

def search_chroma(query: str, k: int = 5):
    """
    Use the question to search for the k most relevant text chunks in ChromaDB
    k=5 means returning the 5 most relevant chunks
    """
    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )
    results = db.similarity_search(query, k=k)
    return results

def ask_with_rag(question: str, llm) -> str:
    """
    RAG complete process:
    1. Search for relevant text chunks
    2. Concatenate the text chunks into context
    3. Send the context and question to GPT
    """
    from langchain_core.messages import HumanMessage

    results = search_chroma(question)

    # Concatenate the search results into a context
    context = "\n\n".join([doc.page_content for doc in results])

    # Tell GPT: Use this information to answer the question
    prompt = f"""Use the following context to answer the question.
If the answer is not in the context, say "I don't have that information in the uploaded files."

Context:
{context}

Question: {question}
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content