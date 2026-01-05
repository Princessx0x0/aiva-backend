from typing import Optional, Dict, List, Literal
from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    detail: str = Field(
        description="Error message",
        json_schema_extra={
            "example": "Failed to generate insights."
        }
    )


class InsightResponse(BaseModel):
    spending_summary: Dict[str, float]
    top_category: str
    emotional_tone: Literal["reassuring", "motivating", "grounding"]
    suggested_action: str
    aiva_insight: str
    checkin_question: Optional[str] = None
    checkin_options: Optional[List[str]] = None

    top_category: str = Field(
        json_schema_extra={"example": "Food"}
    )

    emotional_tone: Literal["reassuring", "motivating", "grounding"] = Field(
        json_schema_extra={"example": "reassuring"}
    )

    suggested_action: str = Field(
        json_schema_extra={
            "example": "Try preparing one extra meal at home this week."
        }
    )

    aiva_insight: str = Field(
        json_schema_extra={
            "example": "It looks like food was your top spending category this week..."
        }
    )

    checkin_question: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "example": "Which of these feels closest to what’s been going on for you lately?"
        }
    )

    checkin_options: Optional[List[str]] = Field(
        default=None,
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
    aiva_followup: str
    detected_emotion: str
    supportive_reframe: str
    next_step_suggestion: str
