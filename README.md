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
- **Web API Service**: Production-ready Flask API with web interface

## Project Structure

```
├── src/
│   ├── build_index.py    # Build FAISS index from documents
│   ├── ingest.py         # Ingest documents into the system
│   ├── rag.py            # Main RAG query interface
│   ├── general_responses.py  # Handle conversational responses
│   └── utils.py          # Utility functions
├── data/
│   └── docs/             # Document storage
├── store/
│   └── faiss/            # FAISS index storage
├── templates/
│   └── index.html        # Web interface template
├── app.py                # Flask web API server
├── deploy.sh             # Production deployment script
└── requirements.txt      # Python dependencies
```

## Quick Start

### Option 1: Web Interface (Recommended)
```bash
./deploy.sh
```
Then open http://localhost:8000 in your browser.

### Option 2: Command Line
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 src/rag.py
```

## Web API Usage

### Endpoints

#### `POST /ask`
Ask a question to the RAG system.

**Request:**
```json
{
  "question": "What is machine learning?"
}
```

**Response:**
```json
{
  "question": "What is machine learning?",
  "question_type": "technical",
  "answer": "Machine learning is a subset of artificial intelligence...",
  "sources": [
    {
      "id": 1,
      "source": "machine_learning_guide.md",
      "page": 1,
      "preview": "Machine learning is a method of data analysis..."
    }
  ],
  "source_count": 1
}
```

#### `GET /health`
Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "3.0-api"
}
```

#### `GET /topics`
Get available topics and examples.

**Response:**
```json
{
  "topics": [
    {
      "name": "Machine Learning",
      "description": "AI, algorithms, models, training",
      "examples": ["What is supervised learning?"]
    }
  ]
}
```

### Web Interface
Visit the root URL (`/`) to access the interactive web interface with:
- Topic overview
- Question input form
- Real-time responses
- Source citations

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

## Development Setup

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Build the FAISS index (if not exists):
```bash
python3 -c "from src.build_index import build_faiss_index; build_faiss_index()"
```

4. Run the Flask API:
```bash
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=8000
```

## Production Deployment

Use the provided deployment script:
```bash
./deploy.sh
```

This will:
- Set up virtual environment
- Install dependencies
- Build FAISS index (if needed)
- Start Gunicorn server on port 8000

## Notes

- Virtual environment (`.venv/`) and cache files are excluded from git via `.gitignore`
- Install dependencies locally; `requirements.txt` defines what's needed
- The system uses local embeddings (BAAI/bge-small-en-v1.5) for privacy and speed