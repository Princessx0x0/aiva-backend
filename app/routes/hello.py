import logging
from fastapi import APIRouter, HTTPException

from app.services.ai_client import get_gemini_client
from app.models.requests import InsightRequest

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/ai/hello")
def ai_hello(req: InsightRequest):
    """
    Simple AI endpoint:
    AIVA greets the user with a warm, encouraging message.
    """
    client = get_gemini_client()

    if not client:
        raise HTTPException(
            status_code=503,
            detail="AI service is temporarily unavailable."
        )

    # Input is now validated by Pydantic model
    user_name = req.name or "friend"

    prompt = (
        f"You are AIVA, a kind financial well-being assistant. "
        f"Greet {user_name} warmly in 2–3 sentences. "
        f"Acknowledge that money can be stressful, but you're here to help "
        f"them understand things step by step. Keep the tone supportive and calm."
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        ai_text = response.text
        return {"aiva_message": ai_text}

    except Exception as e:
        # ✅ FIXED: Use logging instead of print
        logger.error("Error while calling Gemini (hello)", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while generating AIVA's greeting.",
        )
