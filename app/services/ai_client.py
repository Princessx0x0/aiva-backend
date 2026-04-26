from functools import lru_cache
from google import genai
from app.core.config import get_settings


@lru_cache
def get_gemini_client():
    api_key = get_settings().gemini_api_key

    if not api_key:
        return None

    return genai.Client(api_key=api_key)
