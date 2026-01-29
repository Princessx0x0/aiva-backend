import json

from fastapi import APIRouter, HTTPException

from app.models.responses import InsightResponse, ErrorResponse
from app.helpers.json_cleaner import parse_ai_json
from app.helpers.circuit_breaker import gemini_circuit_breaker
from app.services.spending_engine import load_mock_transactions, summarize_spending
from app.services.ai_client import get_gemini_client
from app.services.knowledge_retriever import build_guidance_text, get_checkin_for_category


router = APIRouter()


@router.post(
    "/ai/insights",
    response_model=InsightResponse,
    responses={
        400: {"model": ErrorResponse},
        429: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
        503: {"model": ErrorResponse},
    },
)
def ai_insights() -> InsightResponse:
    """
    Generate an AI-driven financial insight based on mock transaction data.

    Protected by circuit breaker to prevent cascading failures when
    external AI service experiences issues.
    """
    try:
        # ---- 1. Load + summarize spending ----
        transactions = load_mock_transactions()
        totals = summarize_spending(transactions)

        if not totals:
            raise HTTPException(
                status_code=400,
                detail="No spending data available to analyze."
            )

        # ---- 2. Mini intelligence layer ----
        dominant_category = max(totals, key=totals.get)
        total_spend = sum(totals.values())

        if total_spend < 50:
            spend_level = "low"
        elif total_spend < 150:
            spend_level = "moderate"
        else:
            spend_level = "high"

        category_context_map = {
            "Food": (
                "Food often reflects comfort, routine, or convenience spending. "
                "High food spend can be linked to busy schedules, eating out, or emotional comfort."
            ),
            "Transport": (
                "Transport spending usually points to routine commitments, commuting, or a busy season of movement."
            ),
            "Entertainment": (
                "Entertainment can signal a need for rest, joy, or stress relief after demanding weeks."
            ),
            "Shopping": (
                "Shopping may reflect planned upgrades, self-care, or impulse buys driven by mood."
            ),
        }

        category_context = category_context_map.get(
            dominant_category,
            "This category likely reflects a mix of routine needs and emotional decisions."
        )

        # ---- 2b. Retrieve guidance from knowledge base (RAG) ----
        guidance_text = build_guidance_text(
            dominant_category, user_name="friend")

        # Optional check-in question + options (for multi-category patterns)
        checkin_entry = get_checkin_for_category(dominant_category)
        checkin_question = None
        checkin_options = None

        if checkin_entry:
            checkin_question = checkin_entry.get("question")
            checkin_options = checkin_entry.get("options")

        # ---- 3. Convert summary to text for the AI ----
        summary_text = ", ".join(
            [f"{cat}: £{amt:.2f}" for cat, amt in totals.items()]
        )

        # ---- 4. Build prompt with our mini-intelligence + RAG context ----
        prompt = (
            "You are AIVA, an emotionally intelligent financial well-being assistant.\n\n"
            f"Weekly spending summary: {summary_text}.\n"
            f"Dominant spending category: {dominant_category}.\n"
            f"Approximate total weekly spend: £{total_spend:.2f} ({spend_level} level).\n"
            f"Emotional/contextual note about this category: {category_context}\n\n"
        )

        if guidance_text:
            prompt += (
                "Here are additional coaching guidelines and reflections you should follow "
                "when speaking to the user about this situation:\n"
                f"{guidance_text}\n\n"
            )

        prompt += (
            "TASK 1 — Identify the category with the highest total spending.\n"
            "TASK 2 — Choose the emotional tone the user needs. Options:\n"
            "- reassuring\n- motivating\n- grounding\n\n"
            "TASK 3 — Give ONE gentle and actionable financial suggestion.\n\n"
            "TASK 4 — Write a short (3–4 sentences) narrative insight using the chosen tone.\n"
            "Include empathy, clarity, and emotional awareness.\n\n"
            "FORMAT the response STRICTLY as JSON with:\n"
            "{\n"
            "  'top_category': '',\n"
            "  'emotional_tone': '',\n"
            "  'suggested_action': '',\n"
            "  'aiva_insight': ''\n"
            "}\n"
            "Return only JSON. No commentary."
        )

        # ---- 5. Call Gemini with Circuit Breaker Protection ----
        client = get_gemini_client()

        if not client:
            raise HTTPException(
                status_code=503,
                detail="AI service is temporarily unavailable."
            )

        try:
            # Define the Gemini API call as a callable function
            def call_gemini_api():
                return client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                )

            # Execute through circuit breaker
            response = gemini_circuit_breaker.call(call_gemini_api)
            ai_text = response.text

        except Exception as e:
            error_msg = str(e)

            # Circuit breaker is open (service is down)
            if "Circuit breaker is OPEN" in error_msg:
                print(f"Circuit breaker OPEN: {error_msg}")
                raise HTTPException(
                    status_code=503,
                    detail=error_msg
                )

            # Rate limit error from Gemini API
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                print(f"Gemini API rate limit hit: {repr(e)}")
                raise HTTPException(
                    status_code=429,
                    detail="AI service rate limit exceeded. Please try again in a moment."
                )

            # Generic AI service error
            print(f"Gemini API error: {repr(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to call AI service. Please try again later."
            )

        # ---- 6. Parse JSON safely (using your helper) ----
        try:
            insight_data = parse_ai_json(ai_text)
        except json.JSONDecodeError:
            print("AI returned non-JSON:", ai_text)
            raise HTTPException(
                status_code=500,
                detail="AI returned invalid JSON for insights."
            )

        # ---- 7. Merge backend summary + AI insight ----
        response_body = {
            "spending_summary": totals,
            **insight_data
        }

        # Attach optional check-in data for the frontend / UX layer
        if checkin_question and checkin_options:
            response_body["checkin_question"] = checkin_question
            response_body["checkin_options"] = checkin_options

        return response_body

    except HTTPException:
        # Re-raise HTTP errors (already formatted correctly)
        raise
    except Exception as e:
        # Catch any unexpected errors
        print("Unexpected error in insights generation:", repr(e))
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while generating insights."
        )
