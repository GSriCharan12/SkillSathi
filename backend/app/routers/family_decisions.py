from typing import Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.family import User
from app.security.auth import get_optional_current_user
from app.schemas.common import ApiResponse
from app.schemas.family_decision import (
    DecisionStateUpdate,
    ConcernResolutionRequest,
    SaveTradeRequest,
    FamilyDecisionRoomSnapshot,
)
from app.services.family_decision_service import family_decision_service

router = APIRouter(prefix="/family-decisions", tags=["Family Decision Room"])


@router.get(
    "/{family_id}",
    response_model=ApiResponse[FamilyDecisionRoomSnapshot],
    summary="Get multi-perspective Family Decision Room snapshot"
)
def get_decision_room_snapshot(
    family_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """
    Returns the comprehensive 4-part visual decision snapshot:
    1. Learner Perspective
    2. Parent Perspective
    3. AI Verified Evidence
    4. Shared Decision State (EXPLORING, DISCUSSING, COMPARING, NEEDS_COUNSELLING, INFORMED, DECISION_MADE)
    """
    snapshot = family_decision_service.get_decision_room_snapshot(db, family_id, current_user)
    return ApiResponse(
        success=True,
        message="Retrieved Family Decision Room snapshot",
        data=snapshot
    )


@router.patch(
    "/{family_id}/state",
    response_model=ApiResponse[FamilyDecisionRoomSnapshot],
    summary="Update family consensus state"
)
def update_decision_state(
    family_id: int,
    state_in: DecisionStateUpdate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """
    Updates the shared decision state.
    Allowed states: EXPLORING, DISCUSSING, COMPARING, NEEDS_COUNSELLING, INFORMED, DECISION_MADE.
    """
    snapshot = family_decision_service.update_decision_state(db, family_id, state_in, current_user)
    return ApiResponse(
        success=True,
        message=f"Family decision state updated to {state_in.decision_status}",
        data=snapshot
    )


@router.post(
    "/{family_id}/resolve-concern",
    response_model=ApiResponse[FamilyDecisionRoomSnapshot],
    summary="Mark a specific family concern as resolved"
)
def resolve_family_concern(
    family_id: int,
    req: ConcernResolutionRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """Marks a parental or learner concern as addressed with evidence."""
    snapshot = family_decision_service.resolve_concern(db, family_id, req, current_user)
    return ApiResponse(
        success=True,
        message="Concern marked as resolved",
        data=snapshot
    )


@router.post(
    "/{family_id}/save-trade",
    response_model=ApiResponse[FamilyDecisionRoomSnapshot],
    summary="Save/bookmark a trade in family options ledger"
)
def save_trade_for_family(
    family_id: int,
    req: SaveTradeRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """Bookmarks or removes a trade from family discussion ledger."""
    snapshot = family_decision_service.save_trade(db, family_id, req, current_user)
    return ApiResponse(
        success=True,
        message="Trade saved to family options",
        data=snapshot
    )

