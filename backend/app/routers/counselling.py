"""
SkillSathi - AI Counselling Engine API Router
"""
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, Query, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.common import ApiResponse
from app.services.counselling_service import CounsellingService
from app.utils.response import success_response, error_response

router = APIRouter(prefix="/counselling", tags=["AI Vocational Counselling Engine"])


class DialogueTurnRequest(BaseModel):
    user_message: Optional[str] = None
    message: Optional[str] = None
    user_role: Optional[str] = None
    speaker_role: Optional[str] = None
    user_id: Optional[int] = None
    family_id: Optional[int] = None
    session_id: Optional[int] = None
    active_trade_id: Optional[int] = None
    trade_id: Optional[int] = None
    locale: Optional[str] = None
    language: Optional[str] = None


class EscalationRequest(BaseModel):
    family_id: int
    reason: str
    priority: str = "HIGH"


@router.post(
    "/message",
    summary="Process dialogue turn through 8-step AI counselling pipeline",
    description="Analyzes language, intent, family context, root concerns, retrieves official evidence, and returns an empathetic grounded response."
)
async def process_dialogue_turn(
    request: DialogueTurnRequest,
    db: Session = Depends(get_db)
):
    msg_text = request.user_message or request.message or ""
    if not msg_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user_message cannot be empty."
        )

    role = request.user_role or request.speaker_role or "PARENT"
    trade_id = request.active_trade_id if request.active_trade_id is not None else request.trade_id
    loc = request.locale or request.language or "en-IN"

    response_payload = await CounsellingService.process_dialogue_turn(
        db=db,
        user_message=msg_text.strip(),
        user_role=role,
        user_id=request.user_id,
        family_id=request.family_id,
        session_id=request.session_id,
        active_trade_id=trade_id,
        locale=loc
    )

    return success_response(
        data=response_payload,
        message="AI Counselling response generated successfully."
    )


@router.get(
    "/sessions/{session_id}/history",
    summary="Get chronological message history for a counselling session",
    description="Returns all learner, parent, and AI counsellor messages with cited evidence links."
)
async def get_session_history(
    session_id: int,
    db: Session = Depends(get_db)
):
    history = CounsellingService.get_session_history(db=db, session_id=session_id)
    return success_response(
        data=history,
        message=f"Retrieved {len(history)} messages from session history."
    )


@router.post(
    "/escalate",
    summary="Escalate case to a human vocational counsellor",
    description="Creates a human counsellor appointment request when complex family concerns or missing data require certified expert guidance."
)
async def escalate_to_human(
    request: EscalationRequest,
    db: Session = Depends(get_db)
):
    case = CounsellingService.escalate_to_human_counsellor(
        db=db,
        family_id=request.family_id,
        reason=request.reason,
        priority=request.priority
    )
    return success_response(
        data=case,
        message="Case successfully escalated to certified human vocational counsellor."
    )


@router.get(
    "/suggested-prompts",
    summary="Get tailored starter question chips",
    description="Returns high-relevance starter chips for learners and parents based on family location and active trade."
)
async def get_suggested_prompts(
    role: str = Query("PARENT", description="LEARNER or PARENT"),
    district: Optional[str] = Query("Warangal"),
    trade_title: Optional[str] = Query("Solar PV Project Technician")
):
    if role == "PARENT":
        prompts = [
            f"What is the starting salary for {trade_title} in {district}?",
            f"Can my child study further for a university degree after ITI?",
            f"What is the 1-year job retention rate and contract security?",
            f"Show local ITI colleges near {district} with hostel facilities",
            f"How does career progression look after 5 years?"
        ]
    else:
        prompts = [
            f"What practical hands-on skills will I learn in {trade_title}?",
            f"How much stipend will I earn during NAPS apprenticeship?",
            f"How do I get lateral entry into 2nd year Polytechnic / B.Tech?",
            f"Which top companies hire from ITIs in {district}?",
            f"Compare Solar PV Technician with EV Service Technician"
        ]

    return success_response(
        data={"role": role, "prompts": prompts},
        message="Suggested prompts retrieved."
    )
