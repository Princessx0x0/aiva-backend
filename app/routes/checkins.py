import json
import logging
from fastapi import APIRouter, HTTPException

from app.models.responses import CheckinResponse, ErrorResponse
from app.models.requests import CheckinRequest
from app.services.ai_client import get_gemini_client
from app.helpers.json_cleaner import parse_ai_json
from app.helpers.circuit_breaker import gemini_circuit_breaker

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/ai/checkin",
    response_model=CheckinResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
        503: {"model": ErrorResponse},
    },
)
def ai_checkin(req: CheckinRequest):
    """
    Follow-up endpoint.
    The user has already seen an insight + check-in options
    and has selected one. AIVA responds with a tailored follow-up.
    """
    # Input is now validated by Pydantic model
    user_name = req.name or "friend"
    category = req.category
    selected = req.selected_option

    prompt = (
        "You are AIVA, an emotionally intelligent financial well-being assistant.\n\n"
        f"User name: {user_name}.\n"
        f"Their dominant spending category is: {category}.\n"
        f"They chose this reflection option: \"{selected}\".\n\n"
        "TASK 1 — Acknowledge their feelings with genuine empathy.\n"
        "TASK 2 — Reflect briefly on how this feeling might be connected to their spending.\n"
        "TASK 3 — Offer 1–2 gentle, realistic next steps that support both emotions and budget.\n"
        "TASK 4 — Keep the tone warm, non-judgmental, and grounded.\n\n"
        "FORMAT the response STRICTLY as JSON with:\n"
        "{\n"
        "  'aiva_followup': '',\n"
        "  'detected_emotion': '',\n"
        "  'supportive_reframe': '',\n"
        "  'next_step_suggestion': ''\n"
        "}\n"
        "Return only JSON. No commentary."
    )

    try:
        client = get_gemini_client()

        if not client:
            raise HTTPException(
                status_code=503,
                detail="AI service is temporarily unavailable."
            )

        try:
            def call_gemini_api():
                return client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                )

            response = gemini_circuit_breaker.call(call_gemini_api)
            ai_text = response.text

            if not ai_text:
                raise HTTPException(
                    status_code=500,
                    detail="AI returned an empty response."
                )

        except Exception as e:
            error_msg = str(e)

            if "Circuit breaker is OPEN" in error_msg:
                logger.warning(f"Circuit breaker OPEN: {error_msg}")
                raise HTTPException(status_code=503, detail=error_msg)

            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                logger.warning("Gemini API rate limit hit", exc_info=True)
                raise HTTPException(
                    status_code=429,
                    detail="AI service rate limit exceeded. Please try again in a moment."
                )

            logger.error("Gemini API error", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Failed to call AI service. Please try again later."
            )

        followup_data = parse_ai_json(ai_text)
        return followup_data

    except json.JSONDecodeError:
        logger.error("AI returned non-JSON for check-in followup", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="AI returned invalid JSON for check-in followup."
        )

    except HTTPException:
        raise

    except Exception:
        logger.error("Check-in followup error", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to generate AIVA's follow-up message."
        )
