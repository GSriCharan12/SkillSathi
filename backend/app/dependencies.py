"""
SkillSathi - Dependency Injection
Provides reusable FastAPI dependencies for databases, authentication, and service instances.
"""
from typing import Generator
from sqlalchemy.orm import Session
from fastapi import Depends
from app.database import get_db
from app.services.health_service import HealthService
from app.services.ai_service import AICounsellingService
from app.config import get_settings, Settings


def get_current_settings() -> Settings:
    return get_settings()


def get_health_service() -> HealthService:
    return HealthService()


def get_ai_counselling_service() -> AICounsellingService:
    return AICounsellingService()
