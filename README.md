# RAG Deployment

A Retrieval-Augmented Generation (RAG) system for querying documents using semantic search and language models.

## Features

- **Interactive Chat**: Ask multiple questions in one session
- **Technical Expertise**: Specialized in machine learning, web development, data science, and cloud computing
- **Smart Responses**: Handles conversational questions and redirects to technical topics
- **Rich Knowledge Base**: Comprehensive guides on technology topics
- **Smart Search**: Improved embeddings and chunking for better retrieval
- **Structured Answers**: Clear formatting with source citations for technical questions
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

## Question Types

### ✅ **Technical Questions** (Answered with sources)
- "What is machine learning?"
- "How does React work?"
- "What are cloud computing models?"
- "Explain data science workflow"

### 💬 **Conversational Questions**
- "How are you?" → Friendly response + redirect to technical topics
- "Hello/Hi" → Greeting + offer help with technical topics
- "Thank you" → Polite acknowledgment

### 🚫 **General Knowledge Questions**
- "Where is Paris?"
- "How to cook pasta?"
- "What is the capital of France?"
- **Response**: "I specialize in technical topics... Would you like to ask about ML/web dev/data science/cloud instead?"

## Notes

- Virtual environment (`.venv/`) and cache files are excluded from git via `.gitignore`
- Install dependencies locally; `requirements.txt` defines what's needed