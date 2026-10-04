"""
SkillSathi - Health & Diagnostics Router
Exposes /api/v1/health, /api/v1/health/database, and /api/v1/version.
"""
from fastapi import APIRouter, Depends, status
from app.schemas.common import ApiResponse
from app.schemas.health import HealthStatus, DatabaseHealthStatus, AppVersionInfo
from app.services.health_service import HealthService
from app.dependencies import get_health_service
from app.utils.response import success_response, error_response

router = APIRouter(tags=["Health & Diagnostics"])


@router.get(
    "/health",
    response_model=ApiResponse[HealthStatus],
    summary="Application Health Probe",
    description="Returns runtime liveness, uptime, and core application metadata."
)
async def get_app_health(
    health_service: HealthService = Depends(get_health_service)
):
    health_data = health_service.get_app_health()
    return success_response(
        data=health_data.model_dump(),
        message="SkillSathi application is healthy and active."
    )


@router.get(
    "/health/database",
    response_model=ApiResponse[DatabaseHealthStatus],
    summary="Database Connectivity Check",
    description="Verifies MySQL connection pool, engine dialect, and query latency."
)
async def get_database_health(
    health_service: HealthService = Depends(get_health_service)
):
    db_health = health_service.get_database_health()
    if db_health.connected:
        return success_response(
            data=db_health.model_dump(),
            message="Database connection verified successfully."
        )
    return success_response(
        data=db_health.model_dump(),
        message="Database connection currently offline or unreachable."
    )


@router.get(
    "/version",
    response_model=ApiResponse[AppVersionInfo],
    summary="API and System Version Information",
    description="Returns product version, AI provider configuration, and SIH problem statement context."
)
async def get_version_info(
    health_service: HealthService = Depends(get_health_service)
):
    version_data = health_service.get_version_info()
    return success_response(
        data=version_data.model_dump(),
        message="SkillSathi version metadata retrieved."
    )
