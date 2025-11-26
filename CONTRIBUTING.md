# Contributing to Expert Review Analysis System

First off, thank you for considering contributing to the Expert Review Analysis System! It's people like you that make this project better for everyone.

---

## ⚠️ AI Development Notice

**This project was developed with AI assistance.** We encourage contributors to:

- Use AI tools (GitHub Copilot, ChatGPT, Claude, etc.) for productivity
- Always review and test AI-generated code before submitting
- Document any AI-assisted contributions in commit messages or PRs
- Ensure all code meets project quality standards regardless of origin

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Testing Guidelines](#testing-guidelines)

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Git
- Basic understanding of Flask, JavaScript, and REST APIs
- Docker (optional, for containerized development)

### Your First Contribution

Unsure where to begin? You can start by looking at:

- **Good First Issue** labels - Simple issues perfect for beginners
- **Help Wanted** labels - Issues where we need community help
- **Documentation** - Improving or expanding documentation
- **Bug Reports** - Reproducing and fixing reported bugs

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates.

When creating a bug report, include:

- **Clear title** - Describe the issue concisely
- **Steps to reproduce** - Detailed steps to reproduce the behavior
- **Expected behavior** - What you expected to happen
- **Actual behavior** - What actually happened
- **Environment details**:
  - OS and version
  - Python version
  - Browser (if frontend issue)
  - Deployment method (self-hosted/Docker)
- **Screenshots** - If applicable
- **Logs** - Relevant error messages or logs

### Suggesting Enhancements

Enhancement suggestions are welcome! Please include:

- **Clear title and description**
- **Use case** - Why this would be useful
- **Proposed solution** - How you envision it working
- **Alternatives considered** - Other approaches you thought about
- **Additional context** - Screenshots, mockups, examples

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following our coding standards
3. **Add tests** if you've added code that should be tested
4. **Update documentation** if you've changed functionality
5. **Ensure tests pass** and code follows style guidelines
6. **Submit your pull request**

## Development Setup

### Self-Hosted Development

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/expert-review-system.git
cd expert-review-system

# Set up Python virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r self-hosted/backend/requirements.txt

# Copy environment template
cp self-hosted/.env.example .env

# Edit .env with your configuration
# Start backend
cd self-hosted/backend
python api_server.py

# Start frontend (separate terminal)
cd self-hosted/frontend
python -m http.server 8000
```

### Docker Development

```bash
# Build image
docker build -t expert-review-dev:latest -f containerized/Dockerfile .

# Run container
docker run -d \
  -p 5000:5000 \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  expert-review-dev:latest
```

## Coding Standards

### Python (Backend)

- **Style**: Follow [PEP 8](https://pep8.org/)
- **Type hints**: Use type hints for all functions
- **Docstrings**: Use Google-style docstrings
- **Imports**: Group in order: stdlib, third-party, local
- **Line length**: Max 120 characters
- **Naming**:
  - `snake_case` for functions and variables
  - `PascalCase` for classes
  - `UPPER_CASE` for constants

Example:

```python
from typing import List, Dict, Optional
import logging

class ReviewAnalyzer:
    """Analyzes reviews for sentiment and themes.

    Attributes:
        config: Configuration object with thresholds
        logger: Logging instance
    """

    def analyze_reviews(self, reviews: List[Dict[str, str]]) -> Dict[str, float]:
        """Analyze list of reviews for sentiment.

        Args:
            reviews: List of review dictionaries with 'text' and 'rating' keys

        Returns:
            Dictionary with sentiment scores

        Raises:
            ValueError: If reviews list is empty
        """
        if not reviews:
            raise ValueError("Reviews list cannot be empty")

        # Implementation
        return {"positive": 0.8, "negative": 0.2}
```

### JavaScript (Frontend)

- **Style**: Use ES6+ features
- **Modules**: Use ES6 modules
- **Naming**:
  - `camelCase` for functions and variables
  - `PascalCase` for classes
  - `UPPER_SNAKE_CASE` for constants
- **Comments**: Use JSDoc for functions
- **Async**: Use async/await over promises

Example:

```javascript
/**
 * Analyzes a media title using the backend API
 * @param {string} title - The media title to analyze
 * @param {string} platform - The platform (imdb, steam, metacritic)
 * @returns {Promise<Object>} Analysis results
 * @throws {Error} If API request fails
 */
async function analyzeTitle(title, platform) {
  if (!title || !platform) {
    throw new Error("Title and platform are required");
  }

  const response = await fetch(`${API_BASE_URL}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name: title, platform }),
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return await response.json();
}
```

### General Best Practices

- **DRY**: Don't Repeat Yourself
- **KISS**: Keep It Simple, Stupid
- **YAGNI**: You Aren't Gonna Need It
- **Error Handling**: Always handle errors gracefully
- **Logging**: Use appropriate log levels
- **Security**: Never commit secrets or API keys
- **Performance**: Consider performance implications

## Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```
feat(api): add rate limiting to analyze endpoint

Implement rate limiting using RateLimiter class to prevent abuse.
Rate limit set to 100 requests per minute.

Closes #123
```

```
fix(frontend): resolve XSS vulnerability in toast notifications

Sanitize user input before displaying in toast messages.
Use textContent instead of innerHTML.

Security issue reported by @username
```

```
docs(readme): update installation instructions for Docker

Add Docker Compose example and troubleshooting section.
```

## Pull Request Process

1. **Update documentation** - README, docstrings, comments
2. **Add tests** - Ensure new code is tested
3. **Update CHANGELOG.md** - Add entry under "Unreleased"
4. **Ensure CI passes** - All tests and linters must pass
5. **Request review** - Tag relevant maintainers
6. **Address feedback** - Respond to review comments
7. **Squash commits** - Keep history clean (if requested)

### PR Title Format

Use the same format as commit messages:

```
feat(scope): add new feature
fix(scope): resolve bug
docs: update documentation
```

### PR Description Template

```markdown
## Description

Brief description of changes

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing

- [ ] Tests added/updated
- [ ] All tests passing
- [ ] Manual testing completed

## Checklist

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings
- [ ] Added tests that prove fix/feature works
- [ ] Dependent changes merged

## Related Issues

Fixes #(issue number)
```

## Testing Guidelines

### Unit Tests (Coming Soon)

```python
# tests/test_review_analyzer.py
import pytest
from expert_review_system import ReviewAnalyzer

def test_analyze_reviews_valid_input():
    """Test review analysis with valid input."""
    analyzer = ReviewAnalyzer()
    reviews = [
        {"text": "Great movie!", "rating": 5},
        {"text": "Terrible experience", "rating": 1}
    ]
    result = analyzer.analyze_reviews(reviews)

    assert "positive" in result
    assert "negative" in result
    assert 0 <= result["positive"] <= 1
```

### Integration Tests

Test API endpoints:

```python
def test_analyze_endpoint():
    """Test /api/analyze endpoint."""
    response = client.post('/api/analyze', json={
        'name': 'Test Movie',
        'platform': 'imdb'
    })

    assert response.status_code == 200
    data = response.json()
    assert 'compatibility' in data
```

### Manual Testing

Before submitting PR:

1. Test both self-hosted and Docker deployments
2. Test on different browsers (Chrome, Firefox, Safari)
3. Test error conditions
4. Test edge cases
5. Check console for errors

## Questions?

Feel free to:

- Open an issue for discussion
- Reach out to maintainers
- Check existing documentation

Thank you for contributing! 🎉
