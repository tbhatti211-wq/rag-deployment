#!/bin/bash

# RAG Deployment Script - Phase 3: Web API Service
# This script sets up and runs the RAG system as a production web service

set -e  # Exit on any error

echo "🚀 Starting RAG Deployment - Phase 3: Web API Service"
echo "=================================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Check if FAISS index exists
if [ ! -f "store/faiss/index.faiss" ]; then
    echo "🔍 Building FAISS index..."
    python3 -c "
from src.build_index import build_faiss_index
print('Building vector index...')
build_faiss_index()
print('✅ Index built successfully!')
"
fi

# Set environment variables
export FLASK_APP=app.py
export FLASK_ENV=production

# Run the Flask application with Gunicorn
echo "🌐 Starting production server..."
echo "📡 Server will be available at: http://localhost:8000"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

# Use Gunicorn for production deployment
gunicorn --bind 0.0.0.0:8000 \
         --workers 4 \
         --worker-class sync \
         --timeout 120 \
         --access-logfile - \
         --error-logfile - \
         --log-level info \
         app:app

echo "✅ Deployment complete!"
echo "🌐 Access your RAG API at: http://localhost:8000"
echo "📖 API Documentation available at: http://localhost:8000/"