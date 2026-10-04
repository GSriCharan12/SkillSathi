"""
SkillSathi - Health and Diagnostics Service
"""
import time
from datetime import datetime, timezone
from app.config import get_settings
from app.database import check_db_health
from app.schemas.health import HealthStatus, DatabaseHealthStatus, AppVersionInfo

_START_TIME = time.time()


class HealthService:
    @staticmethod
    def get_app_health() -> HealthStatus:
        settings = get_settings()
        uptime = round(time.time() - _START_TIME, 2)
        return HealthStatus(
            status="healthy",
            app_name=settings.APP_NAME,
            tagline=settings.APP_TAGLINE,
            version=settings.APP_VERSION,
            environment=settings.APP_ENV,
            uptime_seconds=uptime,
            timestamp=datetime.now(timezone.utc).isoformat()
        )

    @staticmethod
    def get_database_health() -> DatabaseHealthStatus:
        db_status = check_db_health()
        return DatabaseHealthStatus(
            status=db_status.get("status", "unhealthy"),
            connected=db_status.get("connected", False),
            latency_ms=db_status.get("latency_ms", 0.0),
            database_engine=db_status.get("database_engine", "MySQL"),
            database_version=db_status.get("database_version"),
            host=db_status.get("host"),
            database=db_status.get("database"),
            error=db_status.get("error")
        )

    @staticmethod
    def get_version_info() -> AppVersionInfo:
        settings = get_settings()
        return AppVersionInfo(
            app_name=settings.APP_NAME,
            version=settings.APP_VERSION,
            api_version="v1",
            problem_statement="AI-Enabled Career Counselling and Family Decision-Support Platform for Vocational Education",
            ai_provider=settings.AI_PROVIDER,
            ai_model=settings.AI_MODEL,
            build_time="2026-10-04T00:00:00Z",
            supported_locales=settings.SUPPORTED_LOCALES
        )
