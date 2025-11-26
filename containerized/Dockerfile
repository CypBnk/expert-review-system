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

# Copy application code
COPY . .

# Expose backend API port and frontend static server port
EXPOSE 5000
EXPOSE 8000

# Default env (override with runtime .env)
ENV MODEL_NAME=nlptown/bert-base-multilingual-uncased-sentiment \
    RATE_LIMIT_MAX=100 \
    RATE_LIMIT_WINDOW=60 \
    LOG_LEVEL=info

# Start both backend (gunicorn) and static file server via a lightweight supervisor script
CMD ["bash", "-c", "gunicorn -w 4 -b 0.0.0.0:5000 api_server:app --log-level ${LOG_LEVEL} & python -m http.server 8000"]
