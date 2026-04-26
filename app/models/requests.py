from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

_DANGEROUS_PATTERNS = [
    "ignore", "disregard", "forget", "new instructions",
    "system", "admin", "override", "previous instructions",
    "act as", "you are now", "pretend"
]

_ALLOWED_CATEGORIES = [
    "Food", "Transport", "Entertainment", "Shopping",
    "Bills", "Healthcare", "Other"
]


class BaseRequest(BaseModel):
    """Base class providing shared name validation for all request models."""
    name: Optional[str] = Field(
        None,
        max_length=50,
        description="User's name (letters, spaces, hyphens, apostrophes only)"
    )

    @field_validator('name', mode='before')
    @classmethod
    def sanitize_name(cls, v: str | None) -> str | None:
        if v is None:
            return v

        v = v.strip()
        if not v:
            return None

        if not re.match(r"^[a-zA-Z\s'\-]+$", v):
            raise ValueError(
                "Name can only contain letters, spaces, hyphens, and apostrophes"
            )

        v_lower = v.lower()
        for pattern in _DANGEROUS_PATTERNS:
            if pattern in v_lower:
                raise ValueError("Invalid name format")

        return v


class InsightRequest(BaseRequest):
    """Request body for the /ai/hello endpoint."""
    pass


class CheckinRequest(BaseRequest):
    """
    Request body for the /ai/checkin endpoint.
    Sent after the user selects a check-in option in the UI.
    """
    category: str = Field(
        ...,
        max_length=50,
        description="Spending category"
    )

    selected_option: str = Field(
        ...,
        max_length=200,
        description="User's selected check-in option"
    )

    @field_validator('category')
    @classmethod
    def validate_category(cls, v):
        if v not in _ALLOWED_CATEGORIES:
            raise ValueError(
                f"Category must be one of: {', '.join(_ALLOWED_CATEGORIES)}")
        return v
