from pydantic import BaseModel
from typing import Optional


class InsightRequest(BaseModel):
    """
    Request body for the /ai/hello endpoint.
    """
    name: Optional[str] = None


class CheckinRequest(BaseModel):
    """
    Request body for the /ai/checkin endpoint.
    Sent after the user selects a check-in option in the UI.
    """
    name: Optional[str] = None
    category: str
    selected_option: str
