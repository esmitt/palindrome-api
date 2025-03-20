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

    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///../palindrome.db")

    API_PREFIX: str = "/api/v1"

    CORS_ORIGINS: list[str] = ["*"]
    CORS_METHODS: list[str] = ["*"]
    CORS_HEADERS: list[str] = ["*"]

    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "INFO"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
