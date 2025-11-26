# Expert Review Analysis System V2 - Production Dockerfile
# Multi-stage build for smaller runtime image

FROM python:3.11-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps (optional: libcurl, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# Install Python deps first (layer caching)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download BERT model during build to avoid runtime disk space issues
ENV MODEL_NAME=nlptown/bert-base-multilingual-uncased-sentiment \
    MODEL_CACHE_DIR=/app/models
RUN python -c "from transformers import AutoTokenizer, AutoModelForSequenceClassification; \
    AutoTokenizer.from_pretrained('${MODEL_NAME}', cache_dir='${MODEL_CACHE_DIR}'); \
    AutoModelForSequenceClassification.from_pretrained('${MODEL_NAME}', cache_dir='${MODEL_CACHE_DIR}')" || \
    echo "Warning: Failed to pre-download BERT model, will download at runtime"

# Copy application code
COPY . .

# Expose backend API port and frontend static server port
EXPOSE 5000
EXPOSE 8000

# Default env (override with runtime .env)
ENV RATE_LIMIT_MAX=100 \
    RATE_LIMIT_WINDOW=60 \
    LOG_LEVEL=info \
    PYTORCH_NUM_THREADS=2 \
    TRANSFORMERS_VERBOSITY=error

# Start both backend (gunicorn) and static file server via a lightweight supervisor script
# Use fewer workers to reduce memory pressure and improve stability
CMD ["bash", "-c", "gunicorn -w 1 -t 120 -b 0.0.0.0:5000 api_server:app --log-level ${LOG_LEVEL} & python -m http.server 8000"]
