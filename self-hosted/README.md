# Self-Hosted Deployment

This folder contains everything needed to run the Expert Review Analysis System on your own server.

## 📋 Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Modern web browser

## 🚀 Quick Start

### 1. Install Dependencies

The setup script will:

- Create a Python virtual environment
- Install ALL dependencies including PyTorch (~2GB download)
- Copy `.env.example` to `.env` for configuration

**Windows:**

```bash
.\scripts\setup.bat
```

**Linux/Mac:**

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

⚠️ **Note:** The installation may take 5-10 minutes as it downloads PyTorch and other ML dependencies.

### 2. Configure Environment

Copy the example environment file and configure as needed:

```bash
cp .env.example .env
```

Edit `.env` to customize:

- API endpoints
- Rate limiting
- Model configuration
- Optional: External API keys (IMDb, Steam, Metacritic)

### 3. Start Services

**Option A: Start All Services (Recommended)**

Windows:

```bash
.\scripts\start_all.bat
```

Linux/Mac:

```bash
./scripts/start_all.sh
```

**Option B: Start Services Separately**

Backend API (Windows):

```bash
.\scripts\start_server.bat
```

Backend API (Linux/Mac):

```bash
./scripts/start_server.sh
```

Frontend (Windows):

```bash
.\scripts\start_frontend.bat
```

Frontend (Linux/Mac):

```bash
./scripts/start_frontend.sh
```

### 4. Access Application

- **Frontend**: http://localhost:8000
- **API**: http://localhost:5000
- **Health Check**: http://localhost:5000/api/health

## 📁 File Structure

```
self-hosted/
├── backend/
│   ├── api_server.py          # Flask REST API
│   ├── expert_review_system.py # Core analysis engine
│   ├── preference_store.py     # Persistence layer
│   └── requirements.txt        # Python dependencies
├── frontend/
│   ├── index.html             # Main HTML page
│   ├── style.css              # Styles
│   ├── app.js                 # Main app logic
│   ├── config.js              # Configuration
│   ├── api.js                 # API client
│   ├── storage.js             # Local storage
│   └── utils.js               # Utility functions
├── scripts/
│   ├── setup.bat/sh           # Dependency installation
│   ├── start_server.bat/sh    # Start backend
│   ├── start_frontend.bat/sh  # Start frontend
│   └── start_all.bat/sh       # Start everything
├── .env.example               # Environment template
└── README.md                  # This file
```

## 🔧 Configuration

### Environment Variables

All configuration is done through the `.env` file:

```env
# Python Backend
PYTHON_HOST=localhost
PYTHON_PORT=5000

# ML Model
MODEL_NAME=nlptown/bert-base-multilingual-uncased-sentiment
MODEL_CACHE_DIR=./models

# Thresholds
HIGHLY_LIKELY_THRESHOLD=0.8
WORTH_TRYING_THRESHOLD=0.6
PROCEED_CAUTION_THRESHOLD=0.4

# Rate Limiting
RATE_LIMIT_MAX=100
RATE_LIMIT_WINDOW=60

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Optional External APIs
IMDB_API_KEY=your_key_here
STEAM_API_KEY=your_key_here
METACRITIC_API_KEY=your_key_here
```

## 🔒 Security Notes

- Never commit the `.env` file to version control
- API keys are optional but improve scraping reliability
- Use a reverse proxy (nginx/Apache) for production
- Enable HTTPS in production environments
- Configure CORS appropriately for your domain

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Windows - Kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Dependencies Installation Failed

```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install with verbose output
pip install -r requirements.txt -v
```

### Frontend Can't Connect to Backend

1. Check backend is running: http://localhost:5000/api/health
2. Verify `API_BASE_URL` in `.env` matches backend
3. Check CORS settings in `api_server.py`

## 📚 Additional Documentation

- [API Documentation](../docs/API.md)
- [Configuration Guide](../docs/CONFIGURATION.md)
- [Troubleshooting Guide](../docs/TROUBLESHOOTING.md)
