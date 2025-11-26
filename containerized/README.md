# Containerized Deployment (Docker)

This folder contains everything needed to run the Expert Review Analysis System as a Docker container.

---

> **⚠️ AI Development Notice**  
> This Docker configuration and documentation were created with AI assistance (GitHub Copilot, Claude). All content has been reviewed and tested.

---

## 📋 Prerequisites

- Docker 20.10 or higher
- Docker Compose (optional, for easier management)

## 🖥️ System Requirements (Docker)

Minimum:

- **CPU:** 2 vCPUs
- **RAM:** 4 GB
- **Storage:** 15 GB free (image + model cache + logs)
- **Network:** Outbound access to review platforms (IMDb, Steam, Metacritic)

Recommended:

- **CPU:** 4+ cores
- **RAM:** 8–16 GB
- **Storage:** 25 GB free (room for additional models & build layers)
- **GPU:** Not required (CPU inference); optional for future acceleration
- **Disk:** SSD/NVMe preferred for faster model load & container layer extraction

Notes:

- First run performs model cache population; subsequent runs are faster.
- Leave headroom (~2–3 GB) beyond image size to avoid build failures.
- For multiple containers add ~2 GB RAM per extra instance.

## 🚀 Quick Start

### Prerequisites Check

Ensure Docker is running:

```bash
docker --version
docker-compose --version
```

### Option 1: Docker Compose (Recommended)

```bash
# Navigate to containerized directory
cd containerized

# Create environment file
cp .env.example .env

# Start services (builds image automatically)
docker-compose up -d

# View logs
docker-compose logs -f

# Check health
curl http://localhost:5000/api/health

# Stop services
docker-compose down
```

### Option 2: Docker Run (Manual)

```bash
# Build from project root
cd ..
docker build -f containerized/Dockerfile -t expert-review-system:latest .

# Run the container
docker run -d \
  --name expert-review \
  -p 5000:5000 \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  expert-review-system:latest

# Check logs
docker logs -f expert-review

# Stop container
docker stop expert-review
docker rm expert-review
```

⚠️ **Note:** Docker image is ~12.6GB due to PyTorch and ML dependencies.

## 🌐 Access Application

Once running:

- **Frontend**: http://localhost:8000
- **API**: http://localhost:5000
- **Health Check**: http://localhost:5000/api/health

## 📁 File Structure

```
containerized/
├── Dockerfile              # Container definition
├── docker-compose.yml      # Compose configuration
├── .env.example           # Environment template
├── .dockerignore          # Build exclusions
└── README.md              # This file
```

## 🔧 Configuration

### Using Environment Variables

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Configure as needed:

```env
# Application
PYTHON_PORT=5000
FRONTEND_PORT=8000

# ML Model
MODEL_NAME=nlptown/bert-base-multilingual-uncased-sentiment

# Thresholds
HIGHLY_LIKELY_THRESHOLD=0.8
WORTH_TRYING_THRESHOLD=0.6
PROCEED_CAUTION_THRESHOLD=0.4

# Rate Limiting
RATE_LIMIT_MAX=100
RATE_LIMIT_WINDOW=60

# External APIs (Optional)
IMDB_API_KEY=
STEAM_API_KEY=
METACRITIC_API_KEY=
```

### Using Docker Compose

Edit `docker-compose.yml` to customize:

- Port mappings
- Volume mounts
- Resource limits
- Network configuration

## 📊 Container Details

### Image Information

- **Base**: Python 3.11-slim
- **Size**: ~1.2GB
- **Architecture**: Multi-stage build
- **Services**: Gunicorn (API) + Python HTTP Server (Frontend)

### Exposed Ports

- **5000**: Backend API (Gunicorn with 4 workers)
- **8000**: Frontend (Python HTTP Server)

### Persistent Data

Mount a volume for persistent preferences:

```bash
-v /path/to/data:/app/data
```

## 🔒 Security Best Practices

### Production Deployment

1. **Use Secrets Management**

   ```bash
   # Use Docker secrets instead of environment variables
   docker secret create imdb_api_key ./secrets/imdb_key.txt
   ```

2. **Enable HTTPS**

   - Use a reverse proxy (Traefik, nginx, Caddy)
   - Configure SSL certificates
   - Redirect HTTP to HTTPS

3. **Limit Resources**

   ```yaml
   deploy:
     resources:
       limits:
         cpus: "2"
         memory: 2G
   ```

4. **Network Isolation**

   ```yaml
   networks:
     frontend:
     backend:
       internal: true
   ```

5. **Read-Only Filesystem**
   ```bash
   docker run --read-only \
     --tmpfs /tmp \
     -v /app/data \
     expert-review-system:latest
   ```

## 🔍 Health Monitoring

### Health Check

```bash
# Manual check
curl http://localhost:5000/api/health

# Docker health check (built-in)
docker ps --format "table {{.Names}}\t{{.Status}}"
```

### Logs

```bash
# Follow logs
docker logs -f expert-review

# Last 100 lines
docker logs --tail 100 expert-review

# With timestamps
docker logs -t expert-review
```

### Resource Usage

```bash
# Real-time stats
docker stats expert-review

# One-time check
docker stats --no-stream expert-review
```

## 🐛 Troubleshooting

### Container Won't Start

```bash
# Check logs
docker logs expert-review

# Inspect container
docker inspect expert-review

# Try interactive mode
docker run -it expert-review-system:latest /bin/bash
```

### Port Conflicts

```bash
# Check what's using the port
netstat -tuln | grep 5000

# Change port mapping
docker run -p 5001:5000 -p 8001:8000 expert-review-system:latest
```

### Out of Memory

```bash
# Increase memory limit
docker run -m 4g expert-review-system:latest

# Check memory usage
docker stats --format "table {{.Name}}\t{{.MemUsage}}"
```

### Rebuild After Changes

```bash
# Rebuild without cache
docker build --no-cache -t expert-review-system:latest .

# Remove old images
docker image prune -f
```

## 🚀 Advanced Usage

### Multi-Stage Build Optimization

The Dockerfile uses multi-stage builds to minimize image size:

- Build dependencies installed separately
- Only runtime files copied to final image
- Cached layers for faster rebuilds

### Horizontal Scaling

Scale with multiple containers behind a load balancer:

```bash
# Docker Compose scaling
docker-compose up -d --scale api=3

# Kubernetes deployment
kubectl apply -f k8s/deployment.yml
kubectl scale deployment expert-review --replicas=3
```

### Custom Configurations

Override the default command:

```bash
# More workers
docker run expert-review-system:latest \
  gunicorn -w 8 -b 0.0.0.0:5000 api_server:app

# Different log level
docker run -e LOG_LEVEL=DEBUG expert-review-system:latest
```

## 📚 Additional Resources

- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Production Deployment Guide](../docs/PRODUCTION.md)

## 🛠️ Development Hardware (Reference)

Example environment used during development of v2.2.0:

- **CPU:** 8-core desktop (e.g., AMD Ryzen 7 / Intel i7)
- **RAM:** 32 GB
- **GPU:** None (CPU-only inference for BERT sentiment)
- **Storage:** 1 TB NVMe SSD (≥20 GB free for Docker builds & pruning)
- **OS:** Windows 11 + Docker Desktop (WSL2 backend)

Adjust with your actual specs if contributing—section intended for transparency & expectation setting.
