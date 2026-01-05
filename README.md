# AIVA Backend

AI-powered emotional budgeting assistant API.

## Architecture

See `architecture-diagram.jpg` for system design.

## Local Development
```bash
# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Set API key
$env:GEMINI_API_KEY="your-key-here"

# Run server
uvicorn app.main:app --reload
```

## Docker
```bash
# Build
docker build -t aiva-backend:v1 .

# Run
docker run --rm -p 8000:8000 -e GEMINI_API_KEY="your-key" aiva-backend:v1
```

## Deployment

Deployed to Google Cloud Run via CI/CD pipeline.

- **Dev:** `https://aiva-backend-dev-<hash>.run.app`
- **Prod:** `https://aiva-backend-prod-<hash>.run.app`