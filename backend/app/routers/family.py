"""
SkillSathi - Family Decision Room & Onboarding API Router
Manages step-by-step Learner & Parent journeys and generates the combined Family Snapshot.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.common import ApiResponse
from app.schemas.family import (
    LearnerOnboardingUpdate,
    ParentOnboardingUpdate,
    LearnerRead,
    ParentRead,
    FamilySnapshotResponse,
)
from app.services.family_service import FamilyService
from app.security.auth import get_current_user
from app.models.family import User, FamilyRole
from app.utils.response import success_response

router = APIRouter(prefix="/family", tags=["Family Experience & Decision Room"])


@router.post(
    "/learner/onboarding",
    response_model=ApiResponse[LearnerRead],
    summary="Update Learner Onboarding Step & Aspirations",
    description="Saves current learner progress (education, strengths, work environment, salary expectations) with resume support."
)
async def update_learner_onboarding(
    data: LearnerOnboardingUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    learner = FamilyService.update_learner_onboarding(db=db, user=current_user, data=data)
    return success_response(
        data=LearnerRead.model_validate(learner).model_dump(),
        message="Learner onboarding progress saved."
    )


@router.post(
    "/parent/onboarding",
    response_model=ApiResponse[ParentRead],
    summary="Update Parent Priorities & Extract Natural Language Concerns",
    description="Captures parent priorities (income, safety, prestige, degree) and extracts structured concerns from natural language."
)
async def update_parent_onboarding(
    data: ParentOnboardingUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    parent = FamilyService.update_parent_onboarding(db=db, user=current_user, data=data)
    return success_response(
        data=ParentRead.model_validate(parent).model_dump(),
        message="Parent priorities and concerns analyzed and saved."
    )


@router.get(
    "/{family_id}/snapshot",
    response_model=ApiResponse[FamilySnapshotResponse],
    summary="Get combined Family Decision Snapshot",
    description="Generates visual alignment storytelling combining learner interests, parent priorities, detected concerns, and discussion points."
)
async def get_family_snapshot(
    family_id: int,
    db: Session = Depends(get_db)
):
    snapshot = FamilyService.get_family_snapshot(db=db, family_id=family_id)
    return success_response(
        data=FamilySnapshotResponse.model_validate(snapshot).model_dump(),
        message="Family decision snapshot generated successfully."
    )


@router.get(
    "/current/snapshot",
    response_model=ApiResponse[FamilySnapshotResponse],
    summary="Get Family Snapshot for current authenticated session",
    description="Returns the Family Snapshot for the authenticated user's assigned family unit."
)
async def get_my_family_snapshot(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.family_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current user is not associated with an active family room."
        )
    snapshot = FamilyService.get_family_snapshot(db=db, family_id=current_user.family_id)
    return success_response(
        data=FamilySnapshotResponse.model_validate(snapshot).model_dump(),
        message="Current family snapshot retrieved."
    )
