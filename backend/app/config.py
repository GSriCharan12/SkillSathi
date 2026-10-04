"""
SkillSathi - Configuration Module
Manages all environment variables and configuration settings using Pydantic Settings.
"""
from typing import List, Optional, Union
from functools import lru_cache
import os
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application Settings with strict validation and sane defaults."""
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    # Core Application
    APP_NAME: str = "SkillSathi"
    APP_TAGLINE: str = "Explore a future your whole family believes in."
    APP_VERSION: str = "0.1.0"
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "skillsathi_dev_secret_key_change_in_production_2026"

    # Server Configuration
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            if isinstance(v, str):
                import json
                try:
                    return json.loads(v)
                except Exception:
                    return [v]
            return v
        return []

    # Database Configuration (MySQL 8+)
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_DATABASE: str = "skillsathi_db"
    MYSQL_USER: str = "skillsathi_user"
    MYSQL_PASSWORD: str = "skillsathi_password"
    DATABASE_URL: Optional[str] = None

    # Connection Pooling
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 1800

    # AI Provider Settings (gemini | openai | anthropic | ollama | mock)
    AI_PROVIDER: str = "mock"
    AI_API_KEY: Optional[str] = None
    AI_MODEL: str = "gemini-1.5-flash"
    AI_TEMPERATURE: float = 0.2
    AI_MAX_TOKENS: int = 2048

    # Data Sync Settings
    DATA_SYNC_INTERVAL_HOURS: int = 24
    DATA_SYNC_ENABLE_AUTO: bool = False
    GOV_DATA_API_ENDPOINT: str = "https://api.skillsathi.gov.in/v1/mock"

    # Language Configuration (Universal English)
    DEFAULT_LOCALE: str = "en"
    SUPPORTED_LOCALES: List[str] = ["en"]


    def get_database_url(self) -> str:
        """Assemble a valid SQLAlchemy connection URI for MySQL 8+."""
        if self.DATABASE_URL:
            # Handle standard mysql:// to mysql+pymysql:// for PyMySQL driver
            if self.DATABASE_URL.startswith("mysql://"):
                return self.DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)
            return self.DATABASE_URL
        return (
            f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}?charset=utf8mb4"
        )


@lru_cache()
def get_settings() -> Settings:
    """Cached settings singleton."""
    return Settings()
