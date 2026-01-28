# AIVA Backend

Emotion-aware budgeting assistant API built with FastAPI and deployed on Google Cloud Platform.

## Live Deployment

**Development Environment:**  
https://aiva-backend-dev-803184004123.europe-west2.run.app

**API Documentation:**  
https://aiva-backend-dev-803184004123.europe-west2.run.app/docs

## Architecture

AIVA is a containerized FastAPI application deployed to Google Cloud Run with the following infrastructure:

- **Compute:** Cloud Run (serverless containers, europe-west2)
- **Container Registry:** Artifact Registry
- **Secret Management:** Secret Manager (Gemini API key)
- **AI Integration:** Google Gemini API
- **Concurrency:** 5 requests per container (tuned for load)
- **Scaling:** 0-10 instances (auto-scaling)


## Tech Stack

- **Framework:** FastAPI
- **Runtime:** Python 3.11
- **Containerization:** Docker
- **Cloud Platform:** Google Cloud Platform
- **AI Service:** Google Gemini 2.5 Flash
- **Deployment:** Cloud Run (serverless)

## Local Development

### Prerequisites
- Python 3.11+
- Docker Desktop
- Google Cloud SDK (gcloud CLI)
- Gemini API key

### Setup
```bash
# Clone repository
git clone https://github.com/Princessx0x0/aiva-backend.git
cd aiva-backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate    # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Set environment variable
$env:GEMINI_API_KEY="your-gemini-api-key"  # Windows PowerShell
# export GEMINI_API_KEY="your-gemini-api-key"  # macOS/Linux

# Run development server
uvicorn app.main:app --reload
```

Visit http://localhost:8000/docs to see the interactive API documentation.

## Docker

### Build and Run Locally
```bash
# Build image
docker build -t aiva-backend:v1 .

# Run container
docker run --rm -p 8000:8000 -e GEMINI_API_KEY="your-key" aiva-backend:v1

# Test
curl http://localhost:8000/health
```

### Push to Google Artifact Registry
```bash
# Tag for GCP
docker tag aiva-backend:v1 europe-west2-docker.pkg.dev/aiva-platform-dev/aiva/backend:v1

# Push
docker push europe-west2-docker.pkg.dev/aiva-platform-dev/aiva/backend:v1
```

## Cloud Deployment

### Deploy to Cloud Run
```bash
gcloud run deploy aiva-backend-dev \
  --image=europe-west2-docker.pkg.dev/aiva-platform-dev/aiva/backend:latest \
  --platform=managed \
  --region=europe-west2 \
  --allow-unauthenticated \
  --set-secrets=GEMINI_API_KEY=gemini-api-key:latest \
  --min-instances=0 \
  --max-instances=10 \
  --memory=512Mi \
  --cpu=1 \
  --port=8000 \
  --timeout=60 \
  --concurrency=5
```

## API Endpoints

### Health Checks
- `GET /health` - Basic service health (always fast, no external deps)
- `GET /health/ai` - AI service availability check

### Core Endpoints
- `GET /` - Root endpoint with service info
- `POST /v1/ai/hello` - AI greeting endpoint
- `POST /v1/ai/insights` - Generate financial insights (requires transaction data)
- `POST /v1/ai/checkins` - Emotional check-in endpoint

Full API documentation available at `/docs` endpoint.

## Security

- API keys stored in Google Secret Manager (never in code)
- HTTPS enforced via Cloud Run managed certificates
- GDPR-compliant deployment (europe-west2 region)
- Rate limiting: 5 concurrent requests per container

## Current Status

**Production Readiness:** 7/10

**Completed:**
- Containerized application with optimized Docker image
- Deployed to Cloud Run with auto-scaling
- Secure secret management via Secret Manager
- Health endpoints properly designed
- Concurrency tuned for workload (based on load testing)
- Logging enabled via Cloud Logging

**In Progress:**
- CI/CD pipeline with GitHub Actions
- Circuit breaker for external API failures

**Planned:**
- Application-level rate limiting
- Response caching for common requests
- Monitoring and alerting setup
- Production environment separation
- Infrastructure as Code (Terraform)

## Recent Updates

### January 27, 2026 - Load Testing & Resilience
- Underwent external load testing that revealed Gemini API rate limit bottleneck
- Reduced container concurrency from 80 -> 5 for better scaling
- Documented incident and implemented architectural improvements
- See `docs/incident-2026-01-27.md` for full analysis

## Testing
```bash
# Run local tests
pytest

# Test deployed endpoint
curl https://aiva-backend-dev-803184004123.europe-west2.run.app/health

# Test with request body
curl -X POST https://aiva-backend-dev-803184004123.europe-west2.run.app/v1/ai/hello \
  -H "Content-Type: application/json" \
  -d '{"name":"Faith"}'
```

## Documentation

- `docs/incident-2026-01-27.md` - Load test incident report
- `docs/architecture-decisions.md` - Architecture Decision Records (ADRs)
- Architecture diagram: See repository files

## Learning Goals

This project serves as a platform engineering learning vehicle to demonstrate:
- Production-grade cloud infrastructure
- Container orchestration and deployment
- Secret management and security best practices
- Incident response and documentation
- CI/CD automation
- Observability and monitoring

**Target:** Job-ready platform engineering skills by September 2026

## Author

**Princess Faith Okafor**  
Computer Science Student | Graduating September 2026  
GCP Associate Cloud Engineer Certified

- GitHub: [@Princessx0x0](https://github.com/Princessx0x0)
- LinkedIn: [My LinkedIn](https://www.linkedin.com/in/princess-okafor/)

## License

This is a portfolio/learning project.

## Acknowledgments

Built as part of platform engineering skill development journey.