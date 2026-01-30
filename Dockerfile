# =============================================================================
# RAG Deployment Dockerfile
# This file contains instructions to build a Docker image for our RAG API
# =============================================================================

# -----------------------------------------------------------------------------
# BASE IMAGE: Start with Python 3.12 slim
# -----------------------------------------------------------------------------
# "FROM" specifies the base image - like choosing your operating system
# python:3.12-slim is a lightweight Linux with Python pre-installed
# "slim" = smaller size (no extra tools), faster to download
FROM python:3.12-slim

# -----------------------------------------------------------------------------
# METADATA: Add labels for documentation
# -----------------------------------------------------------------------------
LABEL maintainer="tbhatti211@hotmail.com"
LABEL description="RAG Assistant API with document upload"
LABEL version="4.2.0"

# -----------------------------------------------------------------------------
# WORKING DIRECTORY: Set where commands will run inside container
# -----------------------------------------------------------------------------
# WORKDIR creates the directory if it doesn't exist
# All subsequent commands (COPY, RUN) will execute here
WORKDIR /app

# -----------------------------------------------------------------------------
# DEPENDENCIES: Install system packages needed by Python libraries
# -----------------------------------------------------------------------------
# Some Python packages need compilers or system libraries
# Update package list and install required dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------------------------------------------------------
# PYTHON DEPENDENCIES: Copy and install Python packages
# -----------------------------------------------------------------------------
# Copy requirements.txt FIRST (before copying code)
# Why? Docker caches layers - if requirements don't change, 
# it won't reinstall packages (saves time on rebuilds)
COPY requirements.txt .

# Install Python packages
# --no-cache-dir = don't save pip cache (reduces image size)
# --upgrade pip = ensure latest pip version
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# -----------------------------------------------------------------------------
# APPLICATION CODE: Copy all project files
# -----------------------------------------------------------------------------
# Copy everything from your local directory to /app in container
# This includes: app.py, src/, templates/, data/, etc.
COPY . .

# -----------------------------------------------------------------------------
# DATA DIRECTORIES: Ensure required directories exist
# -----------------------------------------------------------------------------
# Create directories that might not exist in the copy
RUN mkdir -p data/uploads store/faiss

# -----------------------------------------------------------------------------
# ENVIRONMENT VARIABLES: Set runtime configuration
# -----------------------------------------------------------------------------
# These can be overridden when running the container
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
ENV WORKERS=2

# -----------------------------------------------------------------------------
# EXPOSE PORT: Document which port the app uses
# -----------------------------------------------------------------------------
# This is documentation only - doesn't actually publish the port
# You still need -p 8000:8000 when running docker run
EXPOSE 8000

# -----------------------------------------------------------------------------
# HEALTH CHECK: Allow Docker to verify app is running
# -----------------------------------------------------------------------------
# Docker will ping /health every 30 seconds
# If it fails 3 times, container is marked unhealthy
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# -----------------------------------------------------------------------------
# STARTUP COMMAND: Run the application
# -----------------------------------------------------------------------------
# This runs when container starts
# Gunicorn serves the Flask app on all interfaces (0.0.0.0)
# --bind 0.0.0.0:8000 = listen on all network interfaces
# --workers 2 = use 2 worker processes for handling requests
# --timeout 120 = allow 120 seconds for requests (needed for LLM calls)
# app:app = module:application (app.py file, app variable)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120", "app:app"]
