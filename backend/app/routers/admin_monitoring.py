"""
SkillSathi - Admin Data Monitoring & Quality Telemetry API Router
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.common import ApiResponse
from app.schemas.sync import AdminMonitoringSummary
from app.services.monitoring_service import MonitoringService
from app.utils.response import success_response

router = APIRouter(prefix="/admin", tags=["Admin Data Monitoring"])


@router.get(
    "/monitoring",
    response_model=ApiResponse[AdminMonitoringSummary],
    summary="Admin Data Monitoring Dashboard Summary",
    description="Aggregated view of source health, sync history, freshness breakdown, and validation quality alerts."
)
async def get_admin_monitoring(
    db: Session = Depends(get_db)
):
    summary_data = MonitoringService.get_admin_summary(db=db)
    return success_response(
        data=AdminMonitoringSummary.model_validate(summary_data).model_dump(),
        message="Admin monitoring telemetry retrieved successfully."
    )
