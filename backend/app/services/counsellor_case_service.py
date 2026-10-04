"""
SkillSathi - Counsellor Case Service & Human Escalation Management
Smart India Hackathon 2026 - Problem Statement 26241
"""
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status

from app.models.counselling import CounsellorCase, CounsellorNote, CounsellingSession
from app.models.family import Family, User, Learner, ParentGuardian, FamilyConcern, FamilyRole
from app.models.trade import Trade
from app.schemas.counsellor_case import (
    CounsellorCaseCreate,
    CounsellorCaseStatusUpdate,
    CounsellorNoteCreate,
    CounsellorCaseOut,
    CounsellorNoteOut,
    CounsellorDashboardSummary,
    ResourceRecommendation,
)
from app.services.live_counselling_hub import live_hub

logger = logging.getLogger(__name__)


class CounsellorCaseService:

    @staticmethod
    def _format_case_out(case: CounsellorCase, include_private_notes: bool = True) -> CounsellorCaseOut:
        """Helper to serialize CounsellorCase into Pydantic schema."""
        location_str = None
        if case.family:
            parts = [p for p in [case.family.district, case.family.state] if p]
            location_str = ", ".join(parts) if parts else None

        # Filter notes based on authorization
        filtered_notes = []
        if case.notes:
            for note in case.notes:
                if note.visibility == "FAMILY_SHARED" or include_private_notes:
                    author_name = note.author.full_name if note.author else "Counsellor"
                    filtered_notes.append(
                        CounsellorNoteOut(
                            id=note.id,
                            case_id=note.case_id,
                            author_id=note.author_id,
                            author_name=author_name,
                            note_text=note.note_text,
                            visibility=note.visibility,
                            is_action_item=note.is_action_item,
                            created_at=note.created_at,
                            updated_at=note.updated_at,
                        )
                    )

        return CounsellorCaseOut(
            id=case.id,
            family_id=case.family_id,
            family_code=case.family.family_code if case.family else None,
            family_name=case.family.family_name if case.family else None,
            location_label=location_str,
            learner_id=case.learner_id,
            learner_name=case.learner.user.full_name if case.learner and case.learner.user else None,
            trade_id=case.trade_id,
            trade_title=case.trade.title if case.trade else None,
            assigned_counsellor_id=case.assigned_counsellor_id,
            assigned_counsellor_name=case.assigned_counsellor.full_name if case.assigned_counsellor else None,
            priority=case.priority or "MEDIUM",
            case_status=case.case_status or "OPEN",
            escalation_reason=case.escalation_reason,
            parent_concerns=case.parent_concerns or [],
            ai_summary=case.ai_summary,
            evidence_shown=case.evidence_shown or [],
            unresolved_questions=case.unresolved_questions or [],
            recommended_resources=case.recommended_resources or [],
            resolution_summary=case.resolution_summary,
            preferred_contact_method=case.preferred_contact_method or "PHONE_CALL",
            contact_details=case.contact_details,
            scheduled_at=case.scheduled_at,
            resolved_at=case.resolved_at,
            created_at=case.created_at,
            updated_at=case.updated_at,
            notes_count=len(case.notes) if case.notes else 0,
            notes=filtered_notes,
        )

    def create_case(
        self,
        db: Session,
        case_in: CounsellorCaseCreate,
        current_user: Optional[User] = None
    ) -> CounsellorCaseOut:
        """Create a new human escalation case from AI counselling or Family Decision Room."""
        family = db.query(Family).filter(Family.id == case_in.family_id).first()
        if not family:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Family ID {case_in.family_id} not found."
            )

        # Infer learner if not passed
        learner_id = case_in.learner_id
        if not learner_id:
            learner = db.query(Learner).filter(Learner.family_id == family.id).first()
            if learner:
                learner_id = learner.id

        # Ingest reported parent concerns if not provided
        parent_concerns = case_in.parent_concerns or []
        if not parent_concerns:
            concerns = db.query(FamilyConcern).filter(
                FamilyConcern.family_id == family.id,
                FamilyConcern.is_addressed == False
            ).all()
            parent_concerns = [c.concern_text for c in concerns]

        db_case = CounsellorCase(
            family_id=family.id,
            learner_id=learner_id,
            trade_id=case_in.trade_id,
            priority=case_in.priority.upper() if case_in.priority else "MEDIUM",
            case_status="OPEN",
            escalation_reason=case_in.escalation_reason,
            parent_concerns=parent_concerns,
            ai_summary=case_in.ai_summary or f"Family requested guidance regarding vocational pathway alignment for trade {case_in.trade_id}.",
            evidence_shown=case_in.evidence_shown or [],
            unresolved_questions=case_in.unresolved_questions or [],
            preferred_contact_method=case_in.preferred_contact_method or "PHONE_CALL",
            contact_details=case_in.contact_details or (current_user.phone_number if current_user else None),
        )
        db.add(db_case)
        db.commit()
        db.refresh(db_case)

        logger.info(f"Created CounsellorCase ID={db_case.id} for Family ID={family.id}")
        return self._format_case_out(db_case, include_private_notes=True)

    def list_cases(
        self,
        db: Session,
        case_status: Optional[str] = None,
        priority: Optional[str] = None,
        counsellor_id: Optional[int] = None,
        family_id: Optional[int] = None,
        current_user: Optional[User] = None
    ) -> List[CounsellorCaseOut]:
        """List cases with privacy filtering for families vs counsellors."""
        query = db.query(CounsellorCase).options(
            joinedload(CounsellorCase.family),
            joinedload(CounsellorCase.learner).joinedload(Learner.user),
            joinedload(CounsellorCase.trade),
            joinedload(CounsellorCase.assigned_counsellor),
            joinedload(CounsellorCase.notes).joinedload(CounsellorNote.author),
        )

        is_counsellor_or_admin = (
            current_user and current_user.role in [FamilyRole.COUNSELLOR.value, FamilyRole.ADMIN.value]
        )

        # Enforce Family Privacy: Non-counsellor authenticated users can ONLY view cases for their authorized family
        if current_user and current_user.role not in [FamilyRole.COUNSELLOR.value, FamilyRole.ADMIN.value]:
            if current_user.family_id:
                query = query.filter(CounsellorCase.family_id == current_user.family_id)
            elif family_id:
                query = query.filter(CounsellorCase.family_id == family_id)
            else:
                return []
        else:
            if family_id:
                query = query.filter(CounsellorCase.family_id == family_id)
            if counsellor_id:
                query = query.filter(CounsellorCase.assigned_counsellor_id == counsellor_id)

        if case_status:
            query = query.filter(CounsellorCase.case_status == case_status.upper())
        if priority:
            query = query.filter(CounsellorCase.priority == priority.upper())

        cases = query.order_by(CounsellorCase.created_at.desc()).all()
        return [self._format_case_out(c, include_private_notes=is_counsellor_or_admin) for c in cases]

    def get_case_detail(
        self,
        db: Session,
        case_id: int,
        current_user: Optional[User] = None
    ) -> CounsellorCaseOut:
        """Fetch full case detail with privacy authorization check."""
        case = db.query(CounsellorCase).options(
            joinedload(CounsellorCase.family),
            joinedload(CounsellorCase.learner).joinedload(Learner.user),
            joinedload(CounsellorCase.trade),
            joinedload(CounsellorCase.assigned_counsellor),
            joinedload(CounsellorCase.notes).joinedload(CounsellorNote.author),
        ).filter(CounsellorCase.id == case_id).first()

        if not case:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Counsellor Case ID {case_id} not found."
            )

        is_counsellor_or_admin = (
            current_user and current_user.role in [FamilyRole.COUNSELLOR.value, FamilyRole.ADMIN.value]
        )

        # Check family authorization
        if not is_counsellor_or_admin and current_user:
            if current_user.family_id != case.family_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied: You can only view cases for your own family."
                )

        return self._format_case_out(case, include_private_notes=is_counsellor_or_admin)

    def assign_case(
        self,
        db: Session,
        case_id: int,
        counsellor_id: int,
        current_user: Optional[User] = None
    ) -> CounsellorCaseOut:
        """Assign a case to a certified human counsellor and update status."""
        case = db.query(CounsellorCase).filter(CounsellorCase.id == case_id).first()
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")

        counsellor = db.query(User).filter(User.id == counsellor_id).first()
        if not counsellor:
            raise HTTPException(status_code=404, detail="Counsellor user not found")

        case.assigned_counsellor_id = counsellor_id
        case.case_status = "ASSIGNED"
        db.commit()
        db.refresh(case)

        # Notify via live hub
        # (Event: "COUNSELLOR_ASSIGNED" -> "Your counsellor has accepted your request.")
        logger.info(f"Assigned Case {case_id} to Counsellor {counsellor.full_name}")
        return self._format_case_out(case, include_private_notes=True)

    def update_status(
        self,
        db: Session,
        case_id: int,
        status_in: CounsellorCaseStatusUpdate,
        current_user: Optional[User] = None
    ) -> CounsellorCaseOut:
        """Update case status (IN_PROGRESS, RESOLVED, FOLLOW_UP_NEEDED)."""
        case = db.query(CounsellorCase).filter(CounsellorCase.id == case_id).first()
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")

        case.case_status = status_in.case_status.upper()
        if status_in.resolution_summary:
            case.resolution_summary = status_in.resolution_summary
        if status_in.scheduled_at:
            case.scheduled_at = status_in.scheduled_at
        if status_in.case_status.upper() == "RESOLVED":
            case.resolved_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(case)
        return self._format_case_out(case, include_private_notes=True)

    def add_note(
        self,
        db: Session,
        case_id: int,
        note_in: CounsellorNoteCreate,
        current_user: Optional[User] = None
    ) -> CounsellorNoteOut:
        """Add a clinical or family-shared counsellor note."""
        case = db.query(CounsellorCase).filter(CounsellorCase.id == case_id).first()
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")

        author_id = current_user.id if current_user else case.assigned_counsellor_id
        db_note = CounsellorNote(
            case_id=case.id,
            author_id=author_id,
            note_text=note_in.note_text,
            visibility=note_in.visibility.upper() if note_in.visibility else "COUNSELLOR_PRIVATE",
            is_action_item=note_in.is_action_item,
        )
        db.add(db_note)
        db.commit()
        db.refresh(db_note)

        author_name = current_user.full_name if current_user else "Certified Counsellor"
        return CounsellorNoteOut(
            id=db_note.id,
            case_id=db_note.case_id,
            author_id=db_note.author_id,
            author_name=author_name,
            note_text=db_note.note_text,
            visibility=db_note.visibility,
            is_action_item=db_note.is_action_item,
            created_at=db_note.created_at,
            updated_at=db_note.updated_at,
        )

    def recommend_resource(
        self,
        db: Session,
        case_id: int,
        resource: ResourceRecommendation,
        current_user: Optional[User] = None
    ) -> CounsellorCaseOut:
        """Add recommended scheme, institute, or qualification guide to case."""
        case = db.query(CounsellorCase).filter(CounsellorCase.id == case_id).first()
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")

        current_resources = case.recommended_resources or []
        current_resources.append(resource.model_dump())
        case.recommended_resources = current_resources
        db.commit()
        db.refresh(case)
        return self._format_case_out(case, include_private_notes=True)

    def get_dashboard_summary(
        self,
        db: Session,
        current_user: Optional[User] = None
    ) -> CounsellorDashboardSummary:
        """Compute summary KPI metrics for the Counsellor Workstation Dashboard."""
        all_cases = db.query(CounsellorCase).options(
            joinedload(CounsellorCase.family),
            joinedload(CounsellorCase.learner).joinedload(Learner.user),
            joinedload(CounsellorCase.trade),
            joinedload(CounsellorCase.assigned_counsellor),
        ).all()

        total = len(all_cases)
        new_cnt = sum(1 for c in all_cases if c.case_status == "OPEN")
        active_cnt = sum(1 for c in all_cases if c.case_status in ["ASSIGNED", "IN_PROGRESS", "FOLLOW_UP_NEEDED"])
        priority_cnt = sum(1 for c in all_cases if c.priority in ["HIGH", "URGENT"] and c.case_status != "RESOLVED")
        resolved_cnt = sum(1 for c in all_cases if c.case_status == "RESOLVED")

        # Sort recent
        sorted_recent = sorted(all_cases, key=lambda x: x.created_at, reverse=True)[:10]
        recent_out = [self._format_case_out(c, include_private_notes=True) for c in sorted_recent]

        return CounsellorDashboardSummary(
            total_cases=total,
            new_cases=new_cnt,
            active_cases=active_cnt,
            priority_cases=priority_cnt,
            resolved_cases=resolved_cnt,
            recent_cases=recent_out,
        )


counsellor_case_service = CounsellorCaseService()
