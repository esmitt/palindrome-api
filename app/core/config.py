import os
from functools import lru_cache

from pydantic import BaseModel


class Settings(BaseModel):
    # main settings
    APP_NAME: str = "Palindrome Detection API"
    DESCRIPTION: str = "API for detecting and managing palindromes in English and Spanish"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")
    DEBUG: bool = ENVIRONMENT == "development"

    # other settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///../default.db")

    API_PREFIX: str = "/api/v1"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
