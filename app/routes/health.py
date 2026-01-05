from fastapi import APIRouter
from app.services.ai_client import get_gemini_client

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
