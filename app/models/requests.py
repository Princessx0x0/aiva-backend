from pydantic import BaseModel, Field, validator
from typing import Optional
import re


class InsightRequest(BaseModel):
    """
    Request body for the /ai/hello endpoint.
    Includes validation to prevent prompt injection.
    """
    name: Optional[str] = Field(
        None,
        max_length=50,
        description="User's name (letters, spaces, hyphens, apostrophes only)"
    )

    @validator('name')
    def sanitize_name(cls, v):
        """Validate and sanitize name input."""
        if v is None:
            return v

        # Remove leading/trailing whitespace
        v = v.strip()

        if not v:
            return None

        # Check for valid characters (letters, spaces, hyphens, apostrophes)
        if not re.match(r"^[a-zA-Z\s'\-]+$", v):
            raise ValueError(
                "Name can only contain letters, spaces, hyphens, and apostrophes"
            )

        # Check for prompt injection patterns
        dangerous_patterns = [
            "ignore", "disregard", "forget", "new instructions",
            "system", "admin", "override", "previous instructions",
            "act as", "you are now", "pretend"
        ]

        v_lower = v.lower()
        for pattern in dangerous_patterns:
            if pattern in v_lower:
                raise ValueError("Invalid name format")

        return v


class CheckinRequest(BaseModel):
    """
    Request body for the /ai/checkin endpoint.
    Sent after the user selects a check-in option in the UI.
    """
    name: Optional[str] = Field(
        None,
        max_length=50,
        description="User's name (letters, spaces, hyphens, apostrophes only)"
    )

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

    @validator('name')
    def sanitize_name(cls, v):
        """Validate and sanitize name input."""
        if v is None:
            return v

        v = v.strip()
        if not v:
            return None

        if not re.match(r"^[a-zA-Z\s'\-]+$", v):
            raise ValueError(
                "Name can only contain letters, spaces, hyphens, and apostrophes"
            )

        dangerous_patterns = [
            "ignore", "disregard", "forget", "new instructions",
            "system", "admin", "override", "previous instructions"
        ]

        v_lower = v.lower()
        for pattern in dangerous_patterns:
            if pattern in v_lower:
                raise ValueError("Invalid name format")

        return v

    @validator('category')
    def validate_category(cls, v):
        """Validate category is from allowed list."""
        allowed_categories = [
            "Food", "Transport", "Entertainment", "Shopping",
            "Bills", "Healthcare", "Other"
        ]

        if v not in allowed_categories:
            raise ValueError(
                f"Category must be one of: {', '.join(allowed_categories)}")

        return v
