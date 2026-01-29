# src/utils.py
import os
import re
from pathlib import Path
from typing import List
from dotenv import load_dotenv

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.document_loaders.unstructured import UnstructuredFileLoader

load_dotenv()

DOCS_DIR = Path("data/docs")

def get_env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()

def load_documents() -> List:
    """Load PDFs, MDs, TXTs from data/docs."""
    docs = []
    for p in DOCS_DIR.glob("*"):
        if p.suffix.lower() in [".pdf"]:
            docs.extend(PyPDFLoader(str(p)).load())
        elif p.suffix.lower() in [".txt", ".md", ".markdown"]:
            # TextLoader can handle plain text; for md use the same (keeps content)
            docs.extend(TextLoader(str(p), encoding="utf-8").load())
        else:
            # fallback for other formats via unstructured (docx/html)
            docs.extend(UnstructuredFileLoader(str(p)).load())
    return docs

def chunk_documents(documents, chunk_size=1000, chunk_overlap=200):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n## ", "\n### ", "\n\n", "\n", ". ", " ", ""],
        length_function=len,
        keep_separator=True
    )
    return splitter.split_documents(documents)

def sanitize_text(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()