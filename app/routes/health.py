from fastapi import APIRouter
from app.services.ai_client import get_gemini_client
from app.helpers.circuit_breaker import gemini_circuit_breaker


router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/health/ai")
def ai_health():
    client = get_gemini_client()

    if not client:
        return {"ai": "unavailable"}

    return {"ai": "available"}


@router.get("/health/circuit-breaker")
def circuit_breaker_status():
    """
    Check circuit breaker status for monitoring.
    Returns current state, failure count, and last failure time.
    """
    return gemini_circuit_breaker.get_state()
