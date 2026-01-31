# RAG Deployment

A Retrieval-Augmented Generation (RAG) system for querying documents using semantic search and language models.

## Features

- **Interactive Chat**: Ask multiple questions in one session with response history
- **Documentation Tab**: Built-in API documentation with endpoints, examples, and system info
- **Modern UI/UX**: Beautiful gradient interface with 30-70 layout (Recent sidebar | Chat panel)
- **Quick Topic Cards**: 4 clickable cards for instant prompts (ML, Web Dev, Data Science, Cloud)
- **Health Dashboard**: System status monitoring with dedicated health check page
- **Technical Expertise**: Specialized in machine learning, web development, data science, and cloud computing
- **Smart Responses**: Handles conversational questions and redirects to technical topics
- **Rich Knowledge Base**: Comprehensive guides on technology topics
- **Smart Search**: Improved embeddings and chunking for better retrieval
- **Structured Answers**: Clear formatting with source citations for technical questions
- **Flexible Models**: Local embeddings with optional OpenAI integration
- **Web API Service**: Production-ready Flask API with web interface
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## Project Structure

```
├── src/
│   ├── build_index.py         # Build FAISS index from documents
│   ├── ingest.py              # Ingest documents into the system
│   ├── rag.py                 # Main RAG query interface
│   ├── general_responses.py    # Handle conversational responses
│   └── utils.py               # Utility functions
├── data/
│   └── docs/                  # Document storage (markdown guides)
│       ├── cloud_computing_guide.md
│       ├── data_science_guide.md
│       ├── machine_learning_guide.md
│       └── web_development_guide.md
├── store/
│   └── faiss/
│       └── index.faiss        # FAISS vector index for semantic search
├── templates/
│   ├── index.html             # Main interactive web interface
│   └── health.html            # Health check dashboard
├── app.py                     # Flask web API server
├── deploy.sh                  # Production deployment script
├── requirements.txt           # Python dependencies
└── README.md                  # This file
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
  "version": "4.0"
}
```

#### `GET /health-ui`
View the interactive health check dashboard with system metrics and status.

**Response:** HTML page displaying system health, response times, version, and available topics.

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
Visit the root URL (`/`) to access the modern, interactive web interface with:

**Main Interface** (`/`):
- Gradient header with system status indicator
- 4 interactive topic cards for quick selections
- 30-70 layout: Recent questions sidebar + chat panel
- Real-time question-answer interface
- Response history for easy reference
- Clear button to reset conversation
- Source citations for transparency
- Responsive design (desktop & mobile)

**Health Dashboard** (`/health-ui`):
- System status with color indicators
- Response time metrics
- Available topics listing
- Back button to main interface

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

### Local Deployment
Use the provided deployment script:
```bash
./deploy.sh
```

This will:
- Set up virtual environment
- Install dependencies
- Build FAISS index (if needed)
- Start Gunicorn server on port 8000

### Docker Deployment

**Build the image:**
```bash
docker build -t rag-assistant:latest .
```

**Run the container:**
```bash
docker run -d -p 8000:8000 \
  --name rag-api \
  -e OPENAI_API_KEY=your_key_here \
  rag-assistant:latest
```

**With persistent storage (recommended):**
```bash
docker run -d -p 8000:8000 \
  --name rag-api \
  -e OPENAI_API_KEY=your_key_here \
  -v $(pwd)/data/uploads:/app/data/uploads \
  -v $(pwd)/store/faiss:/app/store/faiss \
  rag-assistant:latest
```

**View logs:**
```bash
docker logs rag-api -f
```

**Health check:**
```bash
curl http://localhost:8000/health
```

### CI/CD Pipeline

This project uses GitHub Actions for automated builds:

1. **On push to main**: Automatically builds Docker image
2. **Runs tests**: Validates code quality
3. **Pushes to Registry**: Image available at `ghcr.io/tbhatti211-wq/rag-deployment:main`
4. **Versioning**: Tags with commit SHA and semantic versions

**Pull from GitHub Container Registry:**
```bash
docker pull ghcr.io/tbhatti211-wq/rag-deployment:main
```

### Cloud Deployment (AWS ECS)

Coming soon: Automated deployment to AWS ECS Fargate with:
- Auto-scaling containers
- Load balancer with public URL
- Persistent storage with EFS
- Environment variable management
- CloudWatch logging

## Document Upload

The system supports uploading custom documents through the web interface:

**Supported Formats:**
- PDF (`.pdf`)
- Text (`.txt`)
- Markdown (`.md`, `.markdown`)

**Upload via UI:**
1. Click the "📤 Upload" tab
2. Select or drag-and-drop your file
3. Document is automatically processed and added to the knowledge base
4. Immediately queryable through the chat interface

**Upload via API:**
```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@/path/to/document.pdf"
```

**Response:**
```json
{
  "status": "success",
  "message": "Document processed successfully",
  "filename": "document.pdf",
  "chunks_added": 12,
  "total_documents": 5
}
```

## Testing

Run the test suite:
```bash
pytest tests/test_api.py -v
```

Tests cover:
- Health endpoint validation
- Technical question answering
- General question handling
- Web interface accessibility
- Performance benchmarks

## Version History

- **v4.3.0**: Docker containerization + CI/CD pipeline
- **v4.2.0**: Document upload feature
- **v4.1.0**: Comprehensive test suite
- **v3.0-api**: Flask API + web interface
- **v2.0**: Enhanced RAG with smart responses
- **v1.0**: Basic CLI RAG implementation

## Notes

- Virtual environment (`.venv/`) and cache files are excluded from git via `.gitignore`
- Install dependencies locally; `requirements.txt` defines what's needed
- The system uses local embeddings (BAAI/bge-small-en-v1.5) for privacy and speed
- Temperature set to 0 for deterministic responses
- Multi-worker compatible with automatic vector store reloading