<div align="center">

# 🎬 Expert Review Analysis System

### AI-Powered Media Recommendation Engine

[![Version](https://img.shields.io/badge/version-2.2.1-blue.svg)](https://github.com/CypBnk/expert-review-system/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**Analyze movies, TV shows, and video games based on YOUR personal preferences**

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

> **⚠️ AI Development Disclaimer**  
> This project was developed with AI assistance (GitHub Copilot, Claude). While thoroughly tested and validated, users should review code before production deployment. All AI-generated content has been reviewed by human developers.

---

## 📖 Overview

The Expert Review Analysis System uses advanced AI and web scraping to help you discover media that matches your taste. By analyzing professional reviews from IMDb, Steam, and Metacritic, it provides personalized compatibility scores and intelligent recommendations.

### 🎯 Key Highlights

- **🤖 AI-Powered Analysis** - Uses NLP to extract themes and sentiment from reviews
- **🌐 Multi-Platform** - Supports IMDb (movies/TV), Steam (games), and Metacritic
- **🎨 Theme Detection** - Identifies 20+ themes like character development, plot twists, atmosphere
- **📊 Smart Matching** - Compares media themes with your personal preferences
- **🔒 Privacy-First** - All data stored locally, no external tracking
- **🐳 Docker Ready** - Production-ready containerized deployment
- **⚡ Real-Time** - Instant analysis with rate limiting and caching

---

## ✨ Features

### Version 2.2 (BERT Sentiment & Evaluation)

#### 🚀 New in 2.2.0

- Real BERT-based sentiment analysis (nlptown multilingual model)
- Evaluation metadata (`mode`, `model`) surfaced in API & UI
- Improved compatibility scoring using true sentiment distribution
- Docker image now pre-caches model for faster cold starts
- Stability improvements (single Gunicorn worker, limited Torch threads)

### Version 2.1 (Production Ready)

#### 🌟 Core Functionality

- **Real Web Scraping** - Extracts authentic reviews from IMDb, Steam, and Metacritic
- **Advanced Filtering** - Deduplication, spam detection, length validation, repetition removal
- **Extractive Summarization** - Keyword-based content extraction with sentiment scoring
- **Enhanced Theme System** - 20 comprehensive themes with keyword dictionaries
- **Intelligent Recommendations** - Weighted compatibility scoring with detailed explanations

#### 🔧 Technical Features

- **Configuration Management** - Environment-based config with `.env` support
- **Structured Logging** - JSON-formatted logs with context tracking and performance metrics
- **Rate Limiting** - Configurable limits with 429 responses and retry headers
- **Persistence Layer** - JSON-based storage with full CRUD operations
- **Docker Support** - Multi-stage builds, Gunicorn WSGI, health checks
- **REST API** - Complete API with health endpoints, analysis, and preference management

#### 🛡️ Security & Reliability

- **XSS Protection** - Event delegation, input sanitization, XSS-safe DOM manipulation
- **Error Handling** - Comprehensive try-catch blocks throughout codebase
- **Graceful Degradation** - Automatic fallback to mock data on scraping failures
- **Input Validation** - Server-side validation for all inputs
- **CORS Configuration** - Properly configured cross-origin resource sharing

---

## 🚀 Quick Start

### Option 1: Self-Hosted (Local Development)

**Prerequisites:** Python 3.11+, pip

```bash
# Clone the repository
git clone https://github.com/CypBnk/expert-review-system.git
cd expert-review-system

# Navigate to self-hosted folder
cd self-hosted

# Install dependencies (Windows)
.\scripts\setup.bat

# OR on Linux/Mac
chmod +x scripts/setup.sh
./scripts/setup.sh

# Configure environment
cp .env.example .env
# Edit .env with your preferred settings

# Start all services (Windows)
.\scripts\start_all.bat

# OR on Linux/Mac
./scripts/start_all.sh

# Access the application
# Frontend: http://localhost:8000
# API: http://localhost:5000
```

**Note:** Setup installs all dependencies including PyTorch (~2GB). This may take 5-10 minutes on first run.

### Option 2: Docker (Production Ready)

**Prerequisites:** Docker 20.10+, Docker Compose

```bash
# Clone the repository
git clone https://github.com/CypBnk/expert-review-system.git
cd expert-review-system/containerized

# Configure environment
cp .env.example .env
# Edit .env as needed

# Option A: Docker Run
docker build -t expert-review-system:latest .
docker run -d \
  --name expert-review \
  -p 5000:5000 \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  expert-review-system:latest

# Option B: Docker Compose (Recommended)
docker-compose up -d

# Check status
docker-compose ps
docker-compose logs -f

# Access the application
# Frontend: http://localhost:8000
# API: http://localhost:5000
# Health: http://localhost:5000/api/health
```

---

## 📚 Documentation

### For Users

- **[Self-Hosted Deployment Guide](self-hosted/README.md)** - Complete setup for local development
- **[Docker Deployment Guide](containerized/README.md)** - Production containerized deployment
- **[Quick Start Guide](QUICKSTART.md)** - Get up and running in 5 minutes

### For Developers

- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute to the project
- **[Security Policy](SECURITY.md)** - Security best practices and vulnerability reporting
- **[Code of Conduct](CODE_OF_CONDUCT.md)** - Community guidelines
- **[Changelog](CHANGELOG.md)** - Version history and release notes

---

## 🏗️ Architecture

### Tech Stack

**Frontend**

- HTML5 with semantic markup and ARIA accessibility
- CSS3 with modern layouts and responsive design
- Vanilla JavaScript (ES6+) with modular architecture
- LocalStorage for client-side persistence

**Backend**

- Python 3.11+ with type hints
- Flask REST API with CORS support
- Gunicorn WSGI server (production)
- BeautifulSoup4 for web scraping
- Requests library for HTTP operations

**Data & ML**

- PyTorch for deep learning framework
- Transformers (HuggingFace) for NLP models
- pandas & NumPy for data processing
- scikit-learn for machine learning utilities

**Infrastructure**

- Docker multi-stage builds
- Docker Compose for orchestration
- JSON file-based persistence
- Environment-based configuration

### Project Structure

```
expert-review-system/
├── self-hosted/           # Self-hosted deployment
│   ├── backend/          # Python API server
│   ├── frontend/         # HTML/CSS/JS client
│   ├── scripts/          # Setup and start scripts
│   └── README.md
├── containerized/        # Docker deployment
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── .dockerignore
│   └── README.md
├── unneeded-files/       # Development docs (not for production)
├── LICENSE               # MIT License with dependency attribution
├── CONTRIBUTING.md       # Contribution guidelines
├── SECURITY.md          # Security policy
├── CODE_OF_CONDUCT.md   # Community standards
├── CHANGELOG.md         # Version history
├── README.md            # This file
└── .gitignore
```

---

## 🎨 How It Works

1. **Input Media Title** - Enter a movie, TV show, or game name with platform
2. **Web Scraping** - System fetches real reviews from IMDb, Steam, or Metacritic
3. **Review Filtering** - Advanced filtering removes spam, duplicates, and low-quality content
4. **Theme Extraction** - AI analyzes reviews to identify 20+ themes (plot twists, atmosphere, etc.)
5. **Sentiment Analysis** - NLP models determine positive/negative sentiment for each theme
6. **Preference Matching** - Compares extracted themes with your saved preferences
7. **Compatibility Score** - Generates percentage match with detailed breakdown
8. **Smart Recommendations** - Provides actionable advice: "Highly Likely Match", "Worth Trying", etc.

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Backend Configuration
PYTHON_HOST=localhost
PYTHON_PORT=5000

# ML Model (HuggingFace)
MODEL_NAME=nlptown/bert-base-multilingual-uncased-sentiment
MODEL_CACHE_DIR=./models

# Recommendation Thresholds
HIGHLY_LIKELY_THRESHOLD=0.8
WORTH_TRYING_THRESHOLD=0.6
PROCEED_CAUTION_THRESHOLD=0.4

# Rate Limiting
RATE_LIMIT_MAX=100
RATE_LIMIT_WINDOW=60

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# External APIs (Optional - improves scraping reliability)
IMDB_API_KEY=your_key_here
STEAM_API_KEY=your_key_here
METACRITIC_API_KEY=your_key_here
```

### Supported Themes

- **Narrative**: character_development, moral_complexity, storytelling, plot_twists
- **World Building**: world_building, exploration, innovation, nostalgia
- **Emotional**: emotional_depth, romance, humor, horror, drama
- **Technical**: visual_effects, pacing, dialogue, atmosphere
- **Genre**: mystery, action, philosophy

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Ways to Contribute

- 🐛 **Report bugs** - Open an issue with detailed reproduction steps
- 💡 **Suggest features** - Share your ideas for improvements
- 📝 **Improve docs** - Help make documentation clearer
- 🧪 **Write tests** - Increase test coverage
- 🔧 **Submit PRs** - Fix bugs or implement features

### Development Setup

```bash
# Fork and clone
git clone https://github.com/CypBnk/expert-review-system.git
cd expert-review-system

# Set up Python environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r self-hosted/backend/requirements.txt

# Run tests (when available)
pytest tests/

# Start development servers
cd self-hosted
./scripts/start_all.sh  # Windows: start_all.bat
```

---

## 🖥️ System Requirements (Docker)

These guidelines reflect observed resource usage (PyTorch + Transformers + scraping) for version 2.2.0.

Minimum (functional):

- **CPU:** 2 vCPUs (x86_64)
- **RAM:** 4 GB (may experience slow BERT inference / risk of OOM under load)
- **Storage:** 15 GB free (≈13 GB image + model cache + logs + preferences)
- **Network:** Stable outbound access to IMDb / Steam / Metacritic

Recommended (comfortable):

- **CPU:** 4+ cores (improves parallel scraping and JSON serialization)
- **RAM:** 8–16 GB (room for future model upgrades & multiple analyses)
- **Storage:** 25 GB free (space for additional HF models, build cache)
- **GPU:** Not required (current build runs CPU inference); optional CUDA GPU for future acceleration
- **File System:** SSD/NVMe for faster layer extraction & model load

Operational Notes:

- First container start pre-caches the model; subsequent starts reuse cached weights.
- Keep at least 2–3 GB free above the image size to avoid OS level disk pressure during `docker build`.
- If running multiple containers, allocate +2 GB RAM per additional instance.

## 🛠️ Development Hardware (Reference)

Baseline development environment used for implementing & validating v2.2.0 (provided for transparency – not a requirement):

| Component | Specification                      | Notes                                                                     |
| --------- | ---------------------------------- | ------------------------------------------------------------------------- |
| CPU       | AMD Ryzen 9 5950X (16C / 32T)      | High parallel throughput for scraping & builds                            |
| RAM       | 64 GB DDR4                         | Headroom for larger future NLP models                                     |
| GPU       | NVIDIA RTX 3090 (24 GB VRAM)       | Currently unused (CPU inference); reserved for potential GPU acceleration |
| Storage   | 4 TB NVMe SSD                      | ~20 GB transient free space for Docker layers & model cache               |
| OS        | Windows 11 (Docker Desktop + WSL2) | Cross-tested on Linux (Ubuntu 22.04) for portability                      |

Notes:

- Current release performs sentiment inference on CPU; GPU is optional.
- Specs exceed recommended requirements (see System Requirements) to allow profiling & experimentation.
- Contributors can comfortably develop with the recommended tier in the System Requirements section.

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### Third-Party Licenses

This project uses open-source packages with compatible licenses:

- Flask, pandas, NumPy, scikit-learn, Beautiful Soup, python-dotenv, Gunicorn - **MIT License**
- Flask-CORS - **MIT License**
- PyTorch - **BSD-3-Clause License**
- Transformers - **Apache 2.0 License**

All dependencies are permissive and compatible with commercial use.

---

## 🔒 Security

Security is a priority. Please review our [Security Policy](SECURITY.md) for:

- Supported versions
- Vulnerability reporting process
- Security best practices
- Deployment guidelines

**Never commit `.env` files or API keys to version control.**

---

## 📊 Version History

- **v2.2.1 (Unreleased additions)** – Hybrid AI prep
  - Optional Ollama integration scaffolding (env vars and backend stubs)
  - Use `OLLAMA_ENABLED=true` to try LLM summarization; falls back to extractive

- **v2.2.1** (2025-12-02) - Expanded review extraction capacity to 1000 reviews per platform

- **v2.2.0** (2025-11-26) - BERT sentiment, evaluation metadata, scoring & Docker stability
- **v2.1.1** (2025-11-26) - Frontend enhancements: dynamic loading states with spinners
- **v2.1.0** (2025-11-26) - Production backend with real scraping, filtering, Docker
- **v2.0.0** (2025-11-25) - Security overhaul, backend integration, modular architecture
- **v1.0.0** - Initial release with basic checklist functionality

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

---

## 🙏 Acknowledgments

- **HuggingFace** - For the Transformers library and pre-trained models
- **IMDb, Steam, Metacritic** - For providing review platforms
- **Flask Team** - For the excellent web framework
- **Contributors** - Everyone who has contributed to this project

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/CypBnk/expert-review-system/issues)
- **Discussions**: [GitHub Discussions](https://github.com/CypBnk/expert-review-system/discussions)
- **Security**: See [SECURITY.md](SECURITY.md) for security-related concerns

---

<div align="center">

[⭐ Star this repo](https://github.com/CypBnk/expert-review-system) if you find it helpful!

</div>
