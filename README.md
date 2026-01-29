# RAG Deployment

A Retrieval-Augmented Generation (RAG) system for querying documents using semantic search and language models.

## Features

- **Interactive Chat**: Ask multiple questions in one session
- **Multiple Knowledge Sources**: Machine Learning, Web Development, Data Science, Cloud Computing guides
- **Smart Search**: Improved embeddings and chunking for better retrieval
- **Structured Answers**: Clear formatting with source citations
- **Flexible Models**: Local embeddings with optional OpenAI integration

## Project Structure

```
├── src/
│   ├── build_index.py    # Build FAISS index from documents
│   ├── ingest.py         # Ingest documents into the system
│   ├── rag.py            # Main RAG query interface
│   └── utils.py          # Utility functions
├── data/
│   └── docs/             # Document storage
├── store/
│   └── faiss/            # FAISS index storage
└── requirements.txt      # Python dependencies
```

## Setup

1. Create a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Interactive Mode (Recommended)
```bash
python3 src/rag.py
```
This starts an interactive chat where you can ask multiple questions. Type 'quit', 'exit', or 'q' to stop, or use Ctrl+C.

### Single Question Mode
```bash
python3 src/rag.py "your question here"
```

## Notes

- Virtual environment (`.venv/`) and cache files are excluded from git via `.gitignore`
- Install dependencies locally; `requirements.txt` defines what's needed