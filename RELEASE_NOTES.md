# Release Notes: v2.2.0 – BERT Sentiment & Evaluation Transparency

Major upgrade introducing real BERT-based sentiment analysis, transparent evaluation metadata, refined scoring, and container stability improvements.

## Highlights

- **Real Sentiment**: Integrated nlptown multilingual BERT model with confidence scoring.
- **Evaluation Field**: `/api/analyze` now returns `evaluation.mode` (`bert` or `mock`) and `evaluation.model`.
- **Frontend Indicator**: Result header shows `[BERT-Sentiment Used]` or `[Mock-Data Used]`.
- **Improved Scoring**: Sentiment alignment now based on actual star predictions (1–5 scale).
- **Docker Optimization**: Pre-cached model during build, reduced Gunicorn workers to 1, limited Torch threads (`PYTORCH_NUM_THREADS=2`).
- **Stability**: Removed volume override preventing model reuse, resolved dataclass ordering crash.
- **Metacritic Enhancements**: Modern CSS selectors, up to 30 user reviews extracted reliably.
- **Structured Logging**: JSON logs with analysis timing, recommendation, and evaluation context.

## Changes

- Compatibility recalibration using true average sentiment values.
- Health endpoint version bump to `2.2.0`.
- README + CHANGELOG updated (system requirements + development hardware reference).
- Added evaluation metadata throughout pipeline.

## Fixes

- Dataclass field ordering error causing Gunicorn worker crash.
- Missing `evaluation` in JSON response serialization.
- Container model cache loss due to volume mount conflict.
- Improper sentiment score source (removed placeholder `predicted_score`).

## Performance & Infrastructure

- Faster cold starts via cached model layers.
- Lower memory footprint with single worker model serving.
- Disk usage guidance added (≥15 GB functional, ≥25 GB recommended).

## System Requirements (Docker)

- **Minimum**: 2 vCPUs, 4 GB RAM, 15 GB free storage.
- **Recommended**: 4+ cores, 8–16 GB RAM, 25 GB free, SSD/NVMe.

## Development Hardware Reference

- AMD Ryzen 9 5950X, 64 GB RAM, RTX 3090 (GPU optional), 4 TB NVMe, Windows 11 (WSL2) + Linux cross-test.

## Upgrade Notes

1. Pull latest code: `git pull origin main`.
2. Rebuild Docker image: `docker compose build --no-cache`.
3. Confirm health: `curl http://localhost:5000/api/health`.
4. Validate analysis response includes `evaluation` field.

### Checksum Validation (optional)

Run `docker images | grep expert-review-system` to confirm updated image size and tag usage.

## Next Roadmap (Potential for 2.3.x)

- GPU optional acceleration path.
- Dark mode + accessibility refinements.
- Automated test suite (pytest + integration).
- Embedding-based theme extraction.
