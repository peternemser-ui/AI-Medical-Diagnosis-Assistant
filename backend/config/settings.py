import os
from functools import lru_cache
from typing import Optional, List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    app_name: str = "AI Medical Diagnosis Assistant"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = True

    # API Keys
    openai_api_key: str = ""
    azure_speech_key: str = ""
    azure_speech_region: str = "eastus"

    # Database
    database_url: str = "postgresql://localhost:5432/medical_diagnosis"
    redis_url: str = "redis://localhost:6379"

    # Authentication
    secret_key: str = "change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Rate Limiting
    rate_limit_per_minute: int = 20
    rate_limit_burst: int = 5

    # Email
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    from_email: str = "noreply@medicaldiagnosis.ai"
    from_name: str = "Medical Diagnosis AI"

    # Logging
    log_level: str = "INFO"

    # AI Configuration
    ai_model: str = "gpt-4o"
    ai_temperature: float = 0.3
    ai_max_tokens: int = 2000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Convenience access
settings = get_settings()
