"""
SkillSathi - Counsellor Cases & Real-Time Escalation API Router
Smart India Hackathon 2026 - Problem Statement 26241
"""
from typing import Optional, List
from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.family import User, FamilyRole
from app.security.auth import get_optional_current_user
from app.schemas.common import ApiResponse
from app.schemas.counsellor_case import (
    CounsellorCaseCreate,
    CounsellorCaseAssign,
    CounsellorCaseStatusUpdate,
    CounsellorNoteCreate,
    ResourceRecommendation,
    CounsellorCaseOut,
    CounsellorNoteOut,
    CounsellorDashboardSummary,
)
from app.services.counsellor_case_service import counsellor_case_service
from app.services.live_counselling_hub import live_hub

router = APIRouter(prefix="/counsellor-cases", tags=["Human Counsellor Cases"])


@router.post(
    "",
    response_model=ApiResponse[CounsellorCaseOut],
    status_code=status.HTTP_201_CREATED,
    summary="Create human counsellor escalation case"
)
def create_counsellor_case(
    case_in: CounsellorCaseCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """
    Creates a new case for human counsellor escalation when:
    - User explicitly requests a certified mentor
    - AI lacks verified evidence
    - High family divergence or unresolved questions exist
    """
    case_out = counsellor_case_service.create_case(db, case_in, current_user)
    return ApiResponse(
        success=True,
        message="Counsellor escalation case created successfully",
        data=case_out
    )


@router.get(
    "",
    response_model=ApiResponse[List[CounsellorCaseOut]],
    summary="List counsellor cases with role-based filtering"
)
def list_counsellor_cases(
    case_status: Optional[str] = Query(None, description="OPEN, ASSIGNED, IN_PROGRESS, RESOLVED, FOLLOW_UP_NEEDED"),
    priority: Optional[str] = Query(None, description="LOW, MEDIUM, HIGH, URGENT"),
    counsellor_id: Optional[int] = Query(None),
    family_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """List cases. Families can only view their own cases. Counsellors can view all queues."""
    cases = counsellor_case_service.list_cases(
        db=db,
        case_status=case_status,
        priority=priority,
        counsellor_id=counsellor_id,
        family_id=family_id,
        current_user=current_user,
    )
    return ApiResponse(
        success=True,
        message=f"Retrieved {len(cases)} counsellor cases",
        data=cases
    )


@router.get(
    "/dashboard-summary",
    response_model=ApiResponse[CounsellorDashboardSummary],
    summary="Get Counsellor Workstation Dashboard metrics"
)
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """Returns aggregated case counts and priority queues for counsellor workstation."""
    summary = counsellor_case_service.get_dashboard_summary(db, current_user)
    return ApiResponse(
        success=True,
        message="Retrieved counsellor dashboard summary",
        data=summary
    )


@router.get(
    "/{case_id}",
    response_model=ApiResponse[CounsellorCaseOut],
    summary="Get detailed counsellor case dossier"
)
def get_case_detail(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """Returns full case context including family background, AI transcripts, and evidence."""
    case = counsellor_case_service.get_case_detail(db, case_id, current_user)
    return ApiResponse(
        success=True,
        message="Retrieved counsellor case detail",
        data=case
    )


@router.post(
    "/{case_id}/assign",
    response_model=ApiResponse[CounsellorCaseOut],
    summary="Assign case to a certified counsellor"
)
def assign_case(
    case_id: int,
    assign_in: CounsellorCaseAssign,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """Assigns case and notifies family that counsellor has accepted."""
    updated = counsellor_case_service.assign_case(db, case_id, assign_in.counsellor_id, current_user)
    return ApiResponse(
        success=True,
        message="Case successfully assigned to counsellor",
        data=updated
    )


@router.patch(
    "/{case_id}/status",
    response_model=ApiResponse[CounsellorCaseOut],
    summary="Update case status (IN_PROGRESS, RESOLVED, FOLLOW_UP_NEEDED)"
)
def update_case_status(
    case_id: int,
    status_in: CounsellorCaseStatusUpdate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """Updates case lifecycle status and optional resolution summary."""
    updated = counsellor_case_service.update_status(db, case_id, status_in, current_user)
    return ApiResponse(
        success=True,
        message=f"Case status updated to {status_in.case_status}",
        data=updated
    )


@router.post(
    "/{case_id}/notes",
    response_model=ApiResponse[CounsellorNoteOut],
    summary="Add clinical or family-shared counsellor note"
)
def add_counsellor_note(
    case_id: int,
    note_in: CounsellorNoteCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """Adds a note. Supports COUNSELLOR_PRIVATE or FAMILY_SHARED visibility."""
    note = counsellor_case_service.add_note(db, case_id, note_in, current_user)
    return ApiResponse(
        success=True,
        message="Note added successfully",
        data=note
    )


@router.post(
    "/{case_id}/resources",
    response_model=ApiResponse[CounsellorCaseOut],
    summary="Recommend scheme, institute, or guide to family"
)
def recommend_resource(
    case_id: int,
    resource: ResourceRecommendation,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """Appends verified resource recommendations to the family case."""
    updated = counsellor_case_service.recommend_resource(db, case_id, resource, current_user)
    return ApiResponse(
        success=True,
        message="Resource recommendation added to case",
        data=updated
    )


@router.get(
    "/{case_id}/presence",
    response_model=ApiResponse[dict],
    summary="Inspect live connection presence for a case"
)
def get_case_presence(case_id: int):
    """Returns verified presence stats without fabricating online status."""
    presence = live_hub.get_case_presence(str(case_id))
    return ApiResponse(
        success=True,
        message="Retrieved case connection presence",
        data=presence
    )


# Real-time WebSocket Endpoint for Live Case Sessions
@router.websocket("/live/{case_id}")
async def live_case_websocket(websocket: WebSocket, case_id: int, role: str = "FAMILY"):
    """
    Genuine WebSocket channel for live counsellor <-> family real-time chat & status sync.
    """
    await live_hub.connect_case(websocket, str(case_id), role=role)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo or broadcast message
            await live_hub.broadcast_to_case(
                str(case_id),
                event_type="LIVE_MESSAGE",
                payload={"role": role, "text": data}
            )
    except WebSocketDisconnect:
        live_hub.disconnect_case(websocket, str(case_id))
