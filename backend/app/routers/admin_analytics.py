"""
SkillSathi - Administrator and Programme Analytics Router
Smart India Hackathon 2026 - Problem Statement 26241:
"A dashboard for scheme administrators showing where and why family resistance is concentrated."
"""
from typing import Optional, List
from fastapi import APIRouter, Depends, Query, Response, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.family import User, FamilyRole
from app.security.auth import get_optional_current_user
from app.schemas.common import ApiResponse
from app.schemas.admin_analytics import (
    ProgrammeAnalyticsResponse,
    ConcernCategoryStat,
    GeographicConcernHotspot,
    TradeAnalyticsItem,
    CounsellingFunnelStage,
)
from app.services.admin_analytics_service import admin_analytics_service
from app.services.live_counselling_hub import live_hub

router = APIRouter(prefix="/admin/analytics", tags=["Scheme Administrator Analytics"])


@router.get(
    "/programme",
    response_model=ApiResponse[ProgrammeAnalyticsResponse],
    summary="Get complete programme analytics and resistance indicators"
)
def get_programme_analytics(
    state: Optional[str] = Query(None, description="Filter by state name"),
    district: Optional[str] = Query(None, description="Filter by district name"),
    trade_id: Optional[int] = Query(None, description="Filter by trade ID"),
    days: int = Query(30, description="Analysis window in days (7, 30, 90, 365)"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """
    Returns full database-derived programme metrics:
    - Overview KPIs (Families counselled, Active sessions, Escalations, Alignment)
    - Concern distribution & severity (Income, Security, Social Perception, Safety, etc.)
    - Transparent Family Resistance Index
    - Geographic hotspots (by state & district)
    - Trade exploration & comparison analytics
    - Multi-stage Counselling conversion funnel
    """
    data = admin_analytics_service.get_programme_analytics(
        db=db,
        state=state,
        district=district,
        trade_id=trade_id,
        days=days
    )
    return ApiResponse(
        success=True,
        message="Programme analytics retrieved successfully",
        data=data
    )


@router.get(
    "/concerns",
    response_model=ApiResponse[List[ConcernCategoryStat]],
    summary="Get concern frequency and severity breakdown"
)
def get_concern_analytics(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """Returns frequency, percentage, and severity for all 8 vocational concern categories."""
    data = admin_analytics_service.get_programme_analytics(db=db)
    return ApiResponse(
        success=True,
        message="Concern analytics retrieved successfully",
        data=data.concerns_breakdown
    )


@router.get(
    "/geographic",
    response_model=ApiResponse[List[GeographicConcernHotspot]],
    summary="Get geographic resistance hotspots"
)
def get_geographic_hotspots(
    state: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """Returns resistance concentration mapped by state and district."""
    data = admin_analytics_service.get_programme_analytics(db=db, state=state)
    return ApiResponse(
        success=True,
        message="Geographic hotspots retrieved successfully",
        data=data.geographic_hotspots
    )


@router.get(
    "/trades",
    response_model=ApiResponse[List[TradeAnalyticsItem]],
    summary="Get trade exploration and comparison telemetry"
)
def get_trade_analytics(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """Returns exploration volume, comparison count, and common concerns per trade."""
    data = admin_analytics_service.get_programme_analytics(db=db)
    return ApiResponse(
        success=True,
        message="Trade analytics retrieved successfully",
        data=data.trade_analytics
    )


@router.get(
    "/funnel",
    response_model=ApiResponse[List[CounsellingFunnelStage]],
    summary="Get multi-stage counselling conversion funnel"
)
def get_counselling_funnel(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """Returns conversion rates across Started -> Concern -> Evidence -> Pathway -> Decided -> Escalated."""
    data = admin_analytics_service.get_programme_analytics(db=db)
    return ApiResponse(
        success=True,
        message="Counselling funnel telemetry retrieved successfully",
        data=data.counselling_funnel
    )


@router.get(
    "/export",
    summary="Export anonymized programme analytics CSV"
)
def export_analytics_csv(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """
    Downloads anonymized CSV dataset of family resistance indicators and district aggregates.
    Strictly preserves privacy by excluding personal identifiers.
    """
    csv_content = admin_analytics_service.export_analytics_csv(db=db)
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=skillsathi_programme_analytics.csv"
        }
    )


# WebSocket channel for live administrative telemetry
@router.websocket("/live")
async def live_admin_analytics_websocket(websocket: WebSocket):
    """Real-time telemetry stream for scheme administrator dashboards."""
    await live_hub.connect_case(websocket, case_id="admin_telemetry", role="ADMIN")
    try:
        while True:
            # Keep socket alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        live_hub.disconnect_case(websocket, case_id="admin_telemetry")
