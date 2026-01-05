import os
from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "AIVA Platform"
    environment: str = os.getenv("ENVIRONMENT", "local")

    gemini_api_key: str | None = os.getenv("GEMINI_API_KEY")


settings = Settings()
