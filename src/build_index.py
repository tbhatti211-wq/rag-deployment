# src/build_index.py
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain.embeddings.base import Embeddings

from utils import load_documents, chunk_documents, get_env

load_dotenv()

STORE_DIR = Path("store/faiss")
STORE_DIR.mkdir(parents=True, exist_ok=True)

def get_embeddings() -> Embeddings:
    backend = get_env("EMBEDDINGS_BACKEND", "LOCAL").upper()
    if backend == "OPENAI":
        from langchain_openai import OpenAIEmbeddings
        model = get_env("OPENAI_EMBED_MODEL", "text-embedding-3-small")
        return OpenAIEmbeddings(model=model, api_key=get_env("OPENAI_API_KEY"))
    else:
        # LOCAL
        from langchain_community.embeddings import HuggingFaceEmbeddings
        model = get_env("LOCAL_EMBED_MODEL", "all-MiniLM-L6-v2")
        return HuggingFaceEmbeddings(model_name=model)

def main():
    docs = load_documents()
    chunks = chunk_documents(docs)
    embeddings = get_embeddings()

    print(f"Building FAISS index from {len(chunks)} chunks...")
    vs = FAISS.from_documents(chunks, embedding=embeddings)
    vs.save_local(str(STORE_DIR))
    print(f"Saved FAISS index to: {STORE_DIR.resolve()}")

if __name__ == "__main__":
    main()