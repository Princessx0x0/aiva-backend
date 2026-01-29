from typing import Optional, Dict, List, Literal
from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Standard error response model."""
    detail: str = Field(
        ...,
        description="Error message",
        json_schema_extra={
            "example": "Failed to generate insights."
        }
    )


class InsightResponse(BaseModel):
    """Response model for AI insights endpoint."""
    spending_summary: Dict[str, float] = Field(
        ...,
        description="Summary of spending by category"
    )

    top_category: str = Field(
        ...,
        description="Category with highest spending",
        json_schema_extra={"example": "Food"}
    )

    emotional_tone: Literal["reassuring", "motivating", "grounding"] = Field(
        ...,
        description="Emotional tone of the response",
        json_schema_extra={"example": "reassuring"}
    )

    suggested_action: str = Field(
        ...,
        description="Actionable suggestion for user",
        json_schema_extra={
            "example": "Try preparing one extra meal at home this week."
        }
    )

    aiva_insight: str = Field(
        ...,
        description="AIVA's personalized insight message",
        json_schema_extra={
            "example": "It looks like food was your top spending category this week..."
        }
    )

    checkin_question: Optional[str] = Field(
        None,
        description="Optional follow-up question for user reflection",
        json_schema_extra={
            "example": "Which of these feels closest to what's been going on for you lately?"
        }
    )

    checkin_options: Optional[List[str]] = Field(
        None,
        description="Optional multiple choice options for check-in",
        json_schema_extra={
            "example": [
                "I've been really stressed or burnt out.",
                "Something exciting or out of the ordinary happened.",
                "I just wanted to enjoy myself, no deeper reason.",
                "I'm not sure / it's a mix of things."
            ]
        }
    )


class CheckinResponse(BaseModel):
    """Response model for check-in follow-up endpoint."""
    aiva_followup: str = Field(
        ...,
        description="AIVA's follow-up message"
    )

    detected_emotion: str = Field(
        ...,
        description="Emotion detected from user's selection"
    )

    supportive_reframe: str = Field(
        ...,
        description="Supportive reframing of the situation"
    )

    next_step_suggestion: str = Field(
        ...,
        description="Suggested next step for user"
    )
