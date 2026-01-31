# RAG Deployment

Production-ready Retrieval-Augmented Generation (RAG) system with web interface, document upload, and Docker deployment.

## Features

- 🚀 **Production-Ready**: Docker + CI/CD + cloud-deployable
- 💬 **Interactive Web UI**: Modern chat interface with response history
- 📤 **Document Upload**: PDF, TXT, Markdown support with auto-processing
- 🔍 **Smart Search**: FAISS vector store with semantic search
- 🎯 **Technical Focus**: Specialized in ML, web dev, data science, cloud computing
- 🐳 **Containerized**: Docker image with health checks and auto-scaling ready
- 🔄 **CI/CD Pipeline**: Automated builds and testing with GitHub Actions
- 📊 **API & Web**: RESTful endpoints + interactive web interface

## Project Structure

```
├── .github/
│   └── workflows/
│       └── docker-build.yml   # CI/CD pipeline for automated builds
├── src/
│   ├── build_index.py         # Build FAISS index from documents
│   ├── ingest.py              # Ingest documents into the system
│   ├── rag.py                 # Main RAG query interface
│   ├── general_responses.py  # Handle conversational responses
│   └── utils.py               # Utility functions
├── data/
│   ├── docs/                  # Default technical guides
│   │   ├── cloud_computing_guide.md
│   │   ├── data_science_guide.md
│   │   ├── machine_learning_guide.md
│   │   └── web_development_guide.md
│   └── uploads/               # User-uploaded documents
├── store/
│   └── faiss/
│       ├── index.faiss        # FAISS vector index
│       └── index.pkl          # Vector store metadata
├── templates/
│   ├── index.html             # Main web interface (chat + upload)
│   └── health.html            # Health check dashboard
├── tests/
│   ├── test_api.py            # API endpoint tests
│   └── requirements.txt       # Test dependencies
├── app.py                     # Flask web API server
├── deploy.sh                  # Local deployment script
├── Dockerfile                 # Container build instructions
├── .dockerignore              # Docker build context exclusions
├── requirements.txt           # Python dependencies
├── PROJECT_EVOLUTION.md       # Project development journey
├── RAG_DEPLOYMENT_PLAN.md     # Deployment phases and progress
└── README.md                  # This file
```

## Quick Start

### Docker (Recommended)
```bash
# Build and run
docker build -t rag-assistant:latest .
docker run -d -p 8000:8000 --name rag-api \
  -e OPENAI_API_KEY=your_key \
  -v $(pwd)/data/uploads:/app/data/uploads \
  -v $(pwd)/store/faiss:/app/store/faiss \
  rag-assistant:latest

# Access at http://localhost:8000
```

### Local Development
```API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Interactive web interface with chat + upload |
| `/ask` | POST | Query the RAG system `{"question": "..."}` |
| `/upload` | POST | Upload documents (PDF/TXT/MD) |
| `/health` | GET | Health check JSON response |
| `/topics` | GET | List available topics |hon3 -c "from src.build_index import build_faiss_index; build_faiss_index()"
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
Deployment

### Docker Commands
```bash
# Build
docker build -t rag-assistant:latest .

# Run (ephemeral storage)
docker run -d -p 8000:8000 --name rag-api \
  -e OPENAI_API_KEY=your_key \
  rag-assistant:latest

# Run (persistent storage - recommended)
docker run -d -p 8000:8000 --name rag-api \
  -e OPENAI_API_KEY=your_key \
  -v $(pwd)/data/uploads:/app/data/uploads \
  -v $(pwd)/store/faiss:/app/store/faiss \
  rag-assistant:latest

# Logs & health
docker logs rag-api -f
curl http://localhost:8000/health
```

### CI/CD Pipeline
- **GitHub Actions**: Auto-builds on push to main
- **Container Registry**: `ghcr.io/tbhatti211-wq/rag-deployment:main`
- **Automated Testing**: Pre-deployment validation

### Cloud Deployment
Supports deployment to:
- AWS ECS Fargate (recommended)
- Railway / Render
- Any Docker-compatible platform**Supported Formats**: PDF, TXT, Markdown

**Via Web UI**: Click "📤 Upload" tab → drag-and-drop file  
**Via API**:
```bash
curl -X POST http://localhost:8000/upload -F "file=@document.pdf"
```

Documents are automatically chunked, embedded, and immediately queryable.

## Technology Stack

- **Backend**: Python 3.12, Flask 3.0.3, Gunicorn 22.0.0
- **AI/ML**: LangChain 0.2.16, OpenAI GPT-4o-mini, FAISS vector store
- **Embeddings**: BAAI/bge-small-en-v1.5 (local) or OpenAI
- **DevOps**: Docker, GitHub Actions, AWS ECS ready
- **Testing**: pytest with API integration tests

## Documentation

- **[PROJECT_EVOLUTION.md](PROJECT_EVOLUTION.md)**: Development journey from CLI to production
- **[RAG_DEPLOYMENT_PLAN.md](RAG_DEPLOYMENT_PLAN.md)**: Deployment phases and architecture

## Version

**Current**: v4.3.0 (Docker + CI/CD)  
**Previous**: v4.2.0 (Upload), v4.1.0 (Tests), v3.0 (API), v2.0 (Smart), v1.0 (CLI)

## License

MIT