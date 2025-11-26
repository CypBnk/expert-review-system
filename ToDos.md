# Open ToDos Snapshot (Expert Review Analysis System V2)

This file captures current open tasks to continue development toward a fully featured production release.

## ✅ Backend Analysis Pipeline (COMPLETED)

- [x] Audit backend methods (confirmed placeholder vs production-grade logic)
- [x] Implement review extraction layer (IMDb via BeautifulSoup, Steam via API, Metacritic via BeautifulSoup with User-Agent rotation and fallbacks)
- [x] Implement `filter_reviews` (dedupe, length threshold 20-5000 chars, spam pattern detection, repetition filtering)
- [x] Implement `summarize_reviews` (extractive summarization by keyword density and sentiment scoring)
- [x] Add theme vocabulary + similarity scoring (20 themes with keyword dictionaries, weighted scoring)
- [x] Implement sentiment alignment (normalized BERT mock scores aligned to user preferences)
- [x] Configurable model + thresholds via `.env` (Config class with MODEL_NAME, thresholds, rate limits)
- [x] Enforce rate limiting in `/api/analyze` with 429 handling and `retry_after`
- [x] Structured logging (JSON lines including `analysis_id`, `duration_ms`, `title`, `recommendation`)
- [x] Backend preference persistence (JSON-based PreferenceStore with full CRUD at `/api/preferences` and `/api/preferences/<id>`)

## Frontend Enhancements

- [x] Dynamic loading states (progress/spinner for metrics and analyses)
- [ ] Accessibility pass (ARIA roles, focus trap in modal, toast announcements via `aria-live`)
- [ ] Theme system / dark mode (toggle + CSS variables)
- [ ] Export analysis report (download JSON/CSV of last analysis)

## Testing & Quality

- [ ] Unit tests (pytest) for: validator, theme similarity, sentiment alignment, summarization logic
- [ ] Integration tests (Flask test client for `/api/analyze`, `/api/metrics`)
- [ ] Frontend smoke tests (Playwright or Cypress – basic analysis flow)
- [ ] Performance profiling (timing decorators around critical pipeline sections)

## Deployment & DevOps

- [x] Fix Self-Hosted deployment:
  - [x] Requirements.txt missing in folder - Fixed: setup.bat/sh now installs from backend/requirements.txt
  - [x] Start-server.bat needs to be updated for Frontend and Backend separation - L28 Updated: python .\\backend\\api_server.py
  - [x] Start-Frontend.bat needs to be updated for Frontend and Backend separation - L27 Updated: cd frontend && python -m http.server 8000
  - [x] Start-all.bat needs to be updated for Frontend and Backend separation - L25 Updated: start "Frontend Server - Port 8000" cmd /k "cd frontend && python -m http.server 8000" | L19 Updated: start "API Server - Port 5000" cmd /k "call venv\Scripts\activate.bat && python .\\backend\\api_server.py"
  - [x] Start-?.sh needs to be updated for Frontend and Backend separation; fix from Start-?.bat integrated into Linux/MacOS files
  - [x] Test-enviroment.\* needs to be updated for Frontend and Backend separation - Fixed: checks frontend/ and backend/ paths
  - [x] API-Server Error - Fixed: setup.bat/sh now installs torch and all dependencies from backend/requirements.txt
- [ ] Real BERT model download & caching layer
- [ ] Web scraping robustness (rotating User-Agent, backoff, error classification)
- [ ] Container healthcheck (Docker `HEALTHCHECK` command for `/api/health`)
- [ ] Centralized config object (merge `.env` + defaults) in Python
- [ ] CI pipeline (lint, tests, build image)

## Documentation

- [ ] Update README with scraping + model setup instructions
- [ ] Add API error codes section
- [ ] Architectural diagram (frontend modules + backend components)
- [ ] Contribution guidelines (`CONTRIBUTING.md`)

## Future / Stretch

- [ ] Authentication & user accounts
- [ ] Preference syncing to backend
- [ ] Advanced NLP theme extraction (topic modeling / embeddings)
- [ ] Persistent analytics dashboard
- [ ] Multi-language support

---

**Last Updated:** 2025-11-26  
**Status:** Backend complete; Frontend loading states implemented; Accessibility, testing, and documentation remaining  
**Version:** 2.1.1
