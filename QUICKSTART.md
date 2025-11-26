# Quick Start Guide

## 5-Minute Setup

### For Self-Hosted

1. **Clone and navigate:**

   ```bash
   git clone https://github.com/yourusername/expert-review-system.git
   cd expert-review-system/self-hosted
   ```

2. **Install dependencies:**

   ```bash
   # Windows
   .\scripts\setup.bat

   # Linux/Mac
   chmod +x scripts/setup.sh && ./scripts/setup.sh
   ```

3. **Configure (optional):**

   ```bash
   cp .env.example .env
   # Edit .env if needed
   ```

4. **Start services:**

   ```bash
   # Windows
   .\scripts\start_all.bat

   # Linux/Mac
   ./scripts/start_all.sh
   ```

5. **Open browser:** http://localhost:8000

### For Docker

1. **Clone and navigate:**

   ```bash
   git clone https://github.com/yourusername/expert-review-system.git
   cd expert-review-system/containerized
   ```

2. **Start with Docker Compose:**

   ```bash
   cp .env.example .env
   docker-compose up -d
   ```

3. **Open browser:** http://localhost:8000

That's it! 🎉

## First Steps

1. **Add a preference:**

   - Click "Manage Preferences"
   - Add your favorite movie/show/game
   - Describe what you love about it

2. **Analyze something new:**

   - Enter a title in the search box
   - Select platform (IMDb/Steam/Metacritic)
   - Click "Analyze"

3. **Get recommendations:**
   - Review compatibility score
   - Read theme breakdowns
   - Check recommendation advice

## Troubleshooting

**Port already in use?**

```bash
# Change ports in .env
PYTHON_PORT=5001
FRONTEND_PORT=8001
```

**Can't connect to API?**

- Check backend is running: http://localhost:5000/api/health
- Verify CORS settings
- Check firewall

**Need help?** Open an issue on GitHub!
