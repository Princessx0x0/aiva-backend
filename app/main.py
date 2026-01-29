import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any

from app.core.logging_config import setup_logging
from app.routes.hello import router as hello_router
from app.routes.insights import router as insights_router
from app.routes.checkins import router as checkins_router
from app.routes.health import router as health_router
from app.services.spending_engine import load_mock_transactions

setup_logging()

app = FastAPI(
    title="AIVA Platform",
    version="2.0.0",
    description="Emotion-aware budgeting assistant API"
)

# Include routers
app.include_router(hello_router, prefix="/v1")
app.include_router(insights_router, prefix="/v1")
app.include_router(checkins_router, prefix="/v1")
app.include_router(health_router)


# FIXED: Environment-based CORS configuration
def get_allowed_origins() -> list:
    """Get allowed origins from environment variable."""
    origins_env = os.getenv("ALLOWED_ORIGINS", "")
    if origins_env:
        return [origin.strip() for origin in origins_env.split(",")]
    # Default for development (restrictive for production)
    return ["http://localhost:3000", "http://localhost:5173"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),  # ✅ FIXED: No more wildcard
    allow_credentials=False,  # ✅ FIXED: Disabled unless needed
    allow_methods=["GET", "POST"],  # ✅ FIXED: Only necessary methods
    allow_headers=["Content-Type"],  # ✅ FIXED: Only necessary headers
)


@app.get("/")
def read_root() -> Dict[str, str]:
    """Root endpoint with service information."""
    return {
        "message": "AIVA is running 🚀",
        "version": "2.0.0",
        "ci_cd": "enabled",
        "deployed_via": "github_actions"
    }


@app.get("/transactions/mock")
def get_mock_transactions() -> List[Dict[str, Any]]:
    """Return mock transaction data for testing."""
    return load_mock_transactions()
