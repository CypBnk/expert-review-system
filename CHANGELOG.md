# Changelog

All notable changes to the Expert Review Analysis System are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Changed

- **Expanded review extraction capacity**
  - IMDb: 20 → 1000 reviews maximum
  - Steam: 20 → 1000 reviews maximum (100 per API page)
  - Metacritic: 30 → 1000 reviews maximum
  - Summarization: 30 → 100 reviews for performance balance
  - Enables richer analysis with larger datasets while maintaining spam filtering

## [2.2.0] - 2025-11-26

### Added

- AI development disclaimer notices across all code and documentation files
- Acknowledgment of AI-assisted development (GitHub Copilot, Claude) with human validation
- **Proper Metacritic scraping for PC games**
  - Updated CSS selectors for 2025 Metacritic redesign (`.c-siteReview`, `.c-siteReviewScore`)
  - Automatic `?platform=pc` parameter addition for game URLs
  - Extracts up to 30 user reviews with ratings, authors, and text
  - Verified working with popular titles (Baldur's Gate 3, tested)
- **Real BERT sentiment analysis integration**
  - Added `BERTSentimentAnalyzer` using `nlptown/bert-base-multilingual-uncased-sentiment`
  - Batch inference with confidence scoring and CPU execution
  - Fallback to mock mode when model load fails (graceful degradation)
- **Evaluation metadata in results**
  - New `evaluation` field returned by `/api/analyze` with `mode` (`bert`|`mock`) and `model`
  - Frontend header now appends `[BERT-Sentiment Used]` or `[Mock-Data Used]`

### Changed

- Compatibility scoring now uses actual BERT average sentiment (1–5 star normalization)
- Sentiment alignment updated to derive from `score` field (removed `predicted_score` placeholder)
- Docker build now pre-downloads ML model during image creation to avoid runtime delays
- Gunicorn configuration reduced to a single worker with `PYTORCH_NUM_THREADS=2` for memory stability

### Fixed

- Dataclass ordering error in `AnalysisResult` (non-default after default) causing worker crash
- Missing `evaluation` field in API response serialization
- Container model caching issue caused by volume override (removed model volume mount)

### Performance / Infrastructure

- Smaller runtime memory footprint by lowering worker count and limiting Torch threads
- Faster cold starts due to pre-cached Transformers model in image layer
- Improved stability under limited disk space (prune strategy + cached model)

### Changed

- **Removed mock data fallbacks** from all platform analyzers
  - IMDbAnalyzer, SteamAnalyzer, MetacriticAnalyzer now return empty lists on failure
  - Improved error handling with specific HTTP, network, and parsing error logging
  - System now fails gracefully without fake data when scraping fails

### Fixed

- **Self-Hosted Deployment Scripts**
  - `setup.bat` and `setup.sh` now install ALL dependencies including PyTorch from `backend/requirements.txt`
  - Fixed missing torch module error that prevented API server startup
  - Updated all Windows batch scripts for frontend/backend separation
  - Updated all Linux/Mac shell scripts for frontend/backend separation
  - Fixed `test_environment.bat` to check correct file paths (`frontend/`, `backend/`)
- **Docker Deployment**

  - Synced `requirements.txt`, `api_server.py`, `expert_review_system.py`, `preference_store.py` to root for Docker builds
  - Verified Docker image builds successfully with all dependencies (12.6GB including PyTorch 2.9.1)
  - Added `.gitignore` comment explaining root-level Python files are for Docker

- **File Structure**
  - Organized AI agent instructions into `.ai-instructions/` folder (excluded from git)
  - Updated `.github/copilot-instructions.md` to reference new location
  - Maintained backward compatibility for GitHub Copilot

### Changed

- Setup scripts now provide clearer output about dependency installation progress
- Both deployment models (Docker and self-hosted) fully validated and working

---

## [2.1.1] - 2025-11-26

### Added

- Dynamic loading states with spinner components
  - Loading spinner CSS with smooth rotation animations
  - Multiple spinner sizes (small, default, large)
  - Loading overlay with backdrop blur effect
  - Button loading state with inline spinner
  - Form loading state that disables all inputs
  - Card loading state with shimmer animation
- Loading utility functions (`showLoading()`, `hideLoading()`, `createSpinner()`)
- Accessibility improvements for loading states
  - `aria-busy` attribute on loading elements
  - `role="status"` for screen reader announcements
  - `aria-label` on spinner elements

### Changed

- Analysis form now shows comprehensive loading states during API calls
- Form inputs automatically disabled during processing to prevent multiple submissions

---

## [2.1.0] - 2025-11-26

### 🎯 Production-Ready Release

Major backend enhancements with real web scraping, advanced filtering, structured logging, and full persistence layer.

### Added

- **Real Web Scraping Implementation**
  - IMDb review extraction using BeautifulSoup with rate limiting
  - Steam API integration for game reviews
  - Metacritic scraping with User-Agent rotation
  - Automatic fallback to mock data on network failures
- **Advanced Review Filtering**
  - Deduplication (case-insensitive text matching)
  - Length validation (20-5000 characters)
  - Spam detection using regex patterns (URLs, advertorial content)
  - Repetition detection (excessive word repetition filtering)
- **Extractive Summarization**
  - Keyword density-based sentence scoring
  - Theme-aligned content extraction
  - Sentiment word detection (positive/negative indicators)
- **Enhanced Theme System**
  - 20 comprehensive themes with keyword dictionaries:
    - character_development, moral_complexity, world_building, storytelling
    - plot_twists, emotional_depth, philosophy, exploration
    - mystery, humor, visual_effects, pacing, dialogue
    - atmosphere, innovation, nostalgia, action, romance, horror, drama
  - Real keyword matching in review text
  - Weighted similarity calculation with bonus for multiple matches
- **Configuration Management**
  - `.env` file support via python-dotenv
  - Centralized Config class with environment variable loading
  - Configurable settings:
    - `MODEL_NAME` - ML model selection
    - `HIGHLY_LIKELY_THRESHOLD`, `WORTH_TRYING_THRESHOLD`, `PROCEED_CAUTION_THRESHOLD`
    - `RATE_LIMIT_MAX`, `RATE_LIMIT_WINDOW`
    - `LOG_LEVEL`, `LOG_FORMAT`
- **API Rate Limiting**
  - 429 (Too Many Requests) responses
  - `retry_after` header in rate limit responses
  - Per-endpoint rate tracking
- **Structured Logging**
  - JSON-formatted log entries
  - Context tracking: `analysis_id`, `title`, `endpoint`
  - Performance metrics: `duration_ms`
  - Configurable log levels via environment
- **Persistence Layer**
  - JSON-based PreferenceStore class (`preference_store.py`)
  - Full CRUD operations:
    - `GET /api/preferences` - List all
    - `POST /api/preferences` - Create new
    - `GET /api/preferences/<id>` - Get by ID
    - `PUT /api/preferences/<id>` - Update
    - `DELETE /api/preferences/<id>` - Delete
  - Auto-initialization with default preferences
  - Automatic directory creation
- **Docker Production Support**
  - Multi-stage Dockerfile optimized for size
  - Gunicorn WSGI server (4 workers)
  - Dual-service container (API + frontend)
  - Health check endpoint at `/api/health`
  - Environment variable configuration
  - Volume mount support for persistent data
- **Documentation**
  - `DOCKER_VALIDATION.md` - Complete validation report
  - `ToDos.md` - Project roadmap and open tasks
  - Updated `.env.example` with all configuration options

### Changed

- **Theme Extraction**: Switched from random selection to keyword-based analysis
- **Sentiment Alignment**: Improved scoring using normalized BERT mock scores
- **API Response Format**: Added structured JSON with better error messages
- **Logging Output**: Standardized to JSON format for better parsing
- **Rate Limiter**: Now configurable via environment variables

### Improved

- **Error Handling**: Comprehensive try-catch blocks throughout backend
- **Code Organization**: Separated concerns (config, storage, analysis)
- **Type Safety**: Added type hints to all Python functions
- **Documentation**: Inline comments and docstrings for all methods

### Fixed

- Frontend/backend field mismatch (`title` vs `name` in API payload)
- Missing import statements
- Incomplete method implementations
- Rate limiter initialization with hardcoded values

### Technical Details

- **Dependencies Added**:
  - `requests>=2.31.0` - HTTP client for web scraping
  - `beautifulsoup4>=4.12.0` - HTML parsing
  - `python-dotenv>=1.0.0` - Environment configuration
  - `gunicorn>=21.2.0` - Production WSGI server
- **Files Added**:
  - `preference_store.py` - Persistence layer
  - `Dockerfile` - Container configuration
  - `DOCKER_VALIDATION.md` - Validation report
  - `CHANGELOG.md` - This file
- **API Enhancements**:
  - Structured error responses with proper HTTP status codes
  - Performance timing in all endpoints
  - Automatic preference reload after CRUD operations

---

## [2.0.0] - 2025-11-25

### 🔒 Security & Architecture Overhaul

Complete refactor addressing critical security issues and implementing modern best practices.

### Added

- **Security Improvements**
  - Event delegation instead of inline event handlers
  - XSS protection via safe DOM manipulation (textContent, createElement)
  - Input sanitization utilities (`sanitizeHTML`, `escapeHTML`)
  - URL validation for external links
- **Error Handling**
  - Try-catch blocks throughout frontend and backend
  - Graceful error messages and user feedback
  - Toast notification system for user alerts
  - Proper HTTP status codes and error responses
- **Data Persistence**
  - LocalStorage integration via `storage.js`
  - Import/export functionality for preferences
  - Auto-save on changes
  - Default preference seeding
- **Backend Integration**
  - Flask API server (`api_server.py`)
  - RESTful endpoints:
    - `POST /api/analyze` - Analyze media titles
    - `GET /api/metrics` - System metrics
    - `GET /api/health` - Health check
    - `GET|POST /api/preferences` - Preference management
  - CORS support for cross-origin requests
  - API client with timeout handling (`api.js`)
- **Frontend Architecture**
  - Modular ES6 structure:
    - `app.js` - Main application logic
    - `config.js` - Configuration constants
    - `storage.js` - Data persistence
    - `api.js` - API communication
    - `utils.js` - Shared utilities
  - Mock API client for development/demo mode
  - Toggle between mock and real API via config
- **Python Backend Enhancements**
  - Type hints throughout codebase
  - Comprehensive logging system
  - Input validation layer (`InputValidator`)
  - Rate limiting class (`RateLimiter`)
  - Dataclasses for structured data (`TitleInfo`, `AnalysisResult`)
  - Missing imports added (`torch`, type annotations)
- **Accessibility**
  - ARIA labels and roles in HTML
  - Semantic HTML structure
  - Keyboard navigation support
- **Documentation**
  - Comprehensive README.md
  - QUICKSTART.md for rapid setup
  - FIXES.md documenting all changes
  - Installation and usage guides

### Changed

- **Project Structure**: Separated frontend modules for better maintainability
- **Event Handling**: Replaced inline handlers with event delegation
- **DOM Updates**: Switched from innerHTML to safe createElement patterns
- **API Communication**: Centralized in dedicated API client class

### Fixed

- XSS vulnerabilities from unsanitized user input
- Missing Python imports (torch, type hints)
- Incomplete method implementations
- No error handling in critical paths
- Memory leaks from improper DOM manipulation
- CORS issues with API requests

### Removed

- Inline event handlers (onclick, onsubmit)
- Direct innerHTML manipulation with user data
- Global function pollution
- Hardcoded configuration values

---

## [1.0.0] - Initial Release

### Features

- Basic media title analysis interface
- Manual preference management
- Simple recommendation engine
- Client-side JavaScript application
- Mock data generation
- Basic HTML/CSS interface

### Known Issues

- Security vulnerabilities (XSS)
- No backend integration
- No data persistence
- Missing error handling
- Incomplete Python backend
- No input validation

---

## Version Comparison

| Feature              | v1.0            | v2.0             | v2.1                            |
| -------------------- | --------------- | ---------------- | ------------------------------- |
| **Security**         | ❌ Basic        | ✅ XSS Protected | ✅ XSS Protected                |
| **Backend**          | ❌ Mock Only    | ✅ Flask API     | ✅ Flask + Real Scraping        |
| **Persistence**      | ❌ None         | ✅ LocalStorage  | ✅ JSON File + LocalStorage     |
| **Error Handling**   | ❌ None         | ✅ Basic         | ✅ Comprehensive                |
| **Logging**          | ❌ Console Only | ✅ Basic         | ✅ Structured JSON              |
| **Rate Limiting**    | ❌ None         | ✅ Scaffolded    | ✅ Enforced                     |
| **Configuration**    | ❌ Hardcoded    | ✅ Config File   | ✅ Environment Variables        |
| **Web Scraping**     | ❌ None         | ❌ Mocked        | ✅ Real (IMDb/Steam/Metacritic) |
| **Theme Analysis**   | ❌ Random       | ✅ Mocked        | ✅ Keyword-Based                |
| **Containerization** | ❌ None         | ❌ None          | ✅ Docker Ready                 |
| **API Versioning**   | ❌ None         | ✅ v2.0.0        | ✅ v2.2.0                       |

---

## Migration Guide

### From v1.0 to v2.0

1. Backend now required - run `python api_server.py`
2. Install Python dependencies: `pip install -r requirements.txt`
3. Frontend files restructured - use new modular structure
4. Update any custom integrations to use new API endpoints

### From v2.0 to v2.1

1. Update `.env` file with new configuration options
2. Preferences now persisted in `./data/preferences.json`
3. Rebuild Docker image if using containers: `docker build -t expert-review-v2 .`
4. Review new API endpoints for preference CRUD operations
5. Configure rate limits via environment variables

---

**For detailed setup instructions, see [README.md](README.md)**  
**For production deployment, see [DOCKER_VALIDATION.md](DOCKER_VALIDATION.md)**
