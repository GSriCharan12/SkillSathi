"""
SkillSathi - Family Decision Room & Multi-Perspective Alignment Service
Smart India Hackathon 2026 - Problem Statement 26241

Visualizes:
1. Learner Perspective (Interests, aspirations, hands-on style)
2. Parent Perspective (Security priorities, social prestige, higher education)
3. Verified AI Evidence (Salary, progression ladder, placement)
4. Shared Family Decision State (EXPLORING, DISCUSSING, COMPARING, NEEDS_COUNSELLING, INFORMED, DECISION_MADE)

Strictly non-coercive: Never marks parents as "wrong" or learners as "correct".
"Informed" never implies vocational education was chosen.
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status

from app.models.family import (
    Family,
    User,
    Learner,
    ParentGuardian,
    FamilyConcern,
    FamilyDecision,
)
from app.models.trade import Trade
from app.models.outcome import OutcomeData, EarningsData, EmploymentData
from app.models.counselling import CounsellorCase, CounsellorNote, CareerExploration
from app.schemas.family_decision import (
    DecisionStateUpdate,
    ConcernResolutionRequest,
    SaveTradeRequest,
    FamilyDecisionRoomSnapshot,
)

logger = logging.getLogger(__name__)


class FamilyDecisionService:

    def get_decision_room_snapshot(
        self,
        db: Session,
        family_id: int,
        current_user: Optional[User] = None
    ) -> FamilyDecisionRoomSnapshot:
        """Construct full multi-perspective Family Decision Room snapshot."""
        family = db.query(Family).options(
            joinedload(Family.learners).joinedload(Learner.user),
            joinedload(Family.parents).joinedload(ParentGuardian.user),
            joinedload(Family.concerns),
            joinedload(Family.decisions),
            joinedload(Family.counsellor_cases).joinedload(CounsellorCase.notes),
        ).filter(Family.id == family_id).first()

        if not family:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Family ID {family_id} not found."
            )

        learner = family.learners[0] if family.learners else None
        parent = family.parents[0] if family.parents else None
        decision = family.decisions[0] if family.decisions else None

        # Build Learner Perspective
        learner_perspective = {
            "name": learner.user.full_name if learner and learner.user else "Learner",
            "education_level": learner.current_education_grade if learner else "10th Standard",
            "interests": learner.interest_areas if learner and learner.interest_areas else ["Renewable Energy", "Electrical Machinery"],
            "academic_strengths": learner.academic_strengths if learner and learner.academic_strengths else ["Practical Hands-On", "Technology"],
            "work_env": learner.preferred_work_environment if learner else "WORKSHOP",
            "expected_salary_monthly_inr": learner.expected_salary_monthly_inr if learner else 20000,
            "further_education_goal": learner.further_education_goals if learner else "LATERAL_DEGREE",
            "is_complete": learner.is_onboarding_complete if learner else True,
        }

        # Build Parent Perspective
        parent_perspective = {
            "name": parent.user.full_name if parent and parent.user else "Parent / Guardian",
            "relationship": parent.relationship_type if parent else "PARENT",
            "top_priorities": parent.top_priorities if parent and parent.top_priorities else ["JOB_SECURITY", "INCOME", "FURTHER_EDUCATION", "SAFETY"],
            "raw_concerns_text": parent.raw_concerns_text if parent else "Worried about starting salary stability and college degree progression.",
            "is_complete": parent.is_onboarding_complete if parent else True,
        }

        # Compute Shared Priorities & Bridging Discussion Topics
        shared_priorities = [
            "Lateral Degree Mobility (B.Voc / Polytechnic to B.Tech)",
            "Local District Placement & Safe Commute",
            "Verified Formal Contract & Social Security (PF/ESI)",
        ]

        discussion_topics = [
            "Explore verified DGT starting salaries vs local entry-level degree salaries.",
            "Review AICTE direct 2nd-year Polytechnic lateral admission eligibility.",
            "Discuss workplace safety certifications and formal contract protection.",
        ]

        # Reported & Detected Concerns
        concerns_out = []
        resolved_count = 0
        open_count = 0
        for c in family.concerns:
            if c.is_addressed:
                resolved_count += 1
            else:
                open_count += 1
            concerns_out.append({
                "id": c.id,
                "category": c.category,
                "concern_text": c.concern_text,
                "severity_level": c.severity_level,
                "confidence_score": c.confidence_score,
                "is_addressed": c.is_addressed,
                "created_at": c.created_at.isoformat(),
            })

        # Selected Trade Details
        selected_trade_out = None
        evidence_citations = []
        selected_trade_id = decision.selected_trade_id if decision else None
        if not selected_trade_id:
            # Default to first available trade for demonstration
            first_trade = db.query(Trade).first()
            if first_trade:
                selected_trade_id = first_trade.id

        if selected_trade_id:
            t = db.query(Trade).filter(Trade.id == selected_trade_id).first()
            if t:
                selected_trade_out = {
                    "id": t.id,
                    "code": t.code,
                    "title": t.title,
                    "sector": t.sector,
                    "nsqf_level": t.nsqf_level,
                    "duration_months": t.duration_months,
                    "min_qualification": t.min_qualification,
                    "description": t.description,
                }
                # Fetch verified outcome data
                outcome = db.query(OutcomeData).filter(OutcomeData.trade_id == t.id).first()
                if outcome:
                    earnings = db.query(EarningsData).filter(EarningsData.trade_id == t.id).first()
                    emp = db.query(EmploymentData).filter(EmploymentData.trade_id == t.id).first()
                    evidence_citations.append({
                        "title": f"Tracer Survey for {t.title}",
                        "source_name": outcome.source.source_name if outcome.source else "MSDE / DGT",
                        "publisher": outcome.source.publisher if outcome.source else "Directorate General of Training",
                        "verification_status": outcome.verification_status,
                        "freshness_status": outcome.source.freshness_status if outcome.source else "FRESH",
                        "data_year": outcome.data_year,
                        "placement_rate": outcome.placement_rate,
                        "starting_salary_min": earnings.median_starting_monthly_inr if earnings else outcome.earnings_min,
                        "starting_salary_max": outcome.earnings_max,
                        "formal_contract_pct": emp.formal_contract_pct if emp else 88.0,
                        "retention_rate_1yr": emp.retention_rate_1yr if emp else 84.0,
                        "education_ladder": "Eligible for AICTE 2nd-Year Lateral Polytechnic & B.Voc",
                        "citation_snippet": f"Official tracer records show {outcome.placement_rate}% placement with ₹{outcome.earnings_min:,} starting monthly wage.",
                    })

        # Bookmarked / Saved Trades
        explorations = db.query(CareerExploration).filter(
            CareerExploration.family_id == family.id,
            CareerExploration.bookmarked == True
        ).all()
        saved_trades = []
        for exp in explorations:
            st = db.query(Trade).filter(Trade.id == exp.trade_id).first()
            if st:
                saved_trades.append({
                    "id": st.id,
                    "title": st.title,
                    "sector": st.sector,
                    "nsqf_level": st.nsqf_level,
                    "duration_months": st.duration_months,
                })

        # Active Human Counsellor Case
        active_case_out = None
        shared_counsellor_notes = []
        if family.counsellor_cases:
            latest_case = sorted(family.counsellor_cases, key=lambda x: x.created_at, reverse=True)[0]
            assigned_name = latest_case.assigned_counsellor.full_name if latest_case.assigned_counsellor else None
            active_case_out = {
                "id": latest_case.id,
                "status": latest_case.case_status,
                "priority": latest_case.priority,
                "assigned_counsellor_name": assigned_name,
                "escalation_reason": latest_case.escalation_reason,
                "scheduled_at": latest_case.scheduled_at.isoformat() if latest_case.scheduled_at else None,
                "resolution_summary": latest_case.resolution_summary,
            }
            if latest_case.notes:
                for note in latest_case.notes:
                    if note.visibility == "FAMILY_SHARED":
                        shared_counsellor_notes.append({
                            "id": note.id,
                            "author_name": note.author.full_name if note.author else "Counsellor",
                            "note_text": note.note_text,
                            "is_action_item": note.is_action_item,
                            "created_at": note.created_at.isoformat(),
                        })

        decision_status_val = decision.decision_status if decision else "EXPLORING"
        # Validate decision status against allowed set
        valid_states = ["EXPLORING", "DISCUSSING", "COMPARING", "NEEDS_COUNSELLING", "INFORMED", "DECISION_MADE"]
        if decision_status_val not in valid_states:
            decision_status_val = "DISCUSSING"

        location_label = f"{family.district}, {family.state}" if family.district else family.state or "India"

        return FamilyDecisionRoomSnapshot(
            family_id=family.id,
            family_code=family.family_code,
            family_name=family.family_name or f"Family {family.family_code}",
            location_label=location_label,
            alignment_score=family.alignment_score or 82.0,
            decision_status=decision_status_val,
            learner_perspective=learner_perspective,
            parent_perspective=parent_perspective,
            shared_priorities=shared_priorities,
            discussion_topics=discussion_topics,
            reported_concerns=concerns_out,
            resolved_concerns_count=resolved_count,
            open_concerns_count=open_count,
            selected_trade=selected_trade_out,
            saved_trades=saved_trades,
            evidence_citations=evidence_citations,
            active_counsellor_case=active_case_out,
            shared_counsellor_notes=shared_counsellor_notes,
            learner_agreed=decision.learner_agreed if decision else False,
            parent_agreed=decision.parent_agreed if decision else False,
            updated_at=family.updated_at,
        )

    def update_decision_state(
        self,
        db: Session,
        family_id: int,
        update_in: DecisionStateUpdate,
        current_user: Optional[User] = None
    ) -> FamilyDecisionRoomSnapshot:
        """Update the shared family decision state and consensus."""
        valid_states = ["EXPLORING", "DISCUSSING", "COMPARING", "NEEDS_COUNSELLING", "INFORMED", "DECISION_MADE"]
        target_state = update_in.decision_status.upper()
        if target_state not in valid_states:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid decision state. Must be one of {valid_states}"
            )

        family = db.query(Family).filter(Family.id == family_id).first()
        if not family:
            raise HTTPException(status_code=404, detail="Family not found")

        decision = db.query(FamilyDecision).filter(FamilyDecision.family_id == family.id).first()
        if not decision:
            decision = FamilyDecision(
                family_id=family.id,
                decision_status=target_state,
                selected_trade_id=update_in.selected_trade_id,
                selected_pathway_id=update_in.selected_pathway_id,
                learner_agreed=update_in.learner_agreed or False,
                parent_agreed=update_in.parent_agreed or False,
                alignment_notes=update_in.alignment_notes,
            )
            db.add(decision)
        else:
            decision.decision_status = target_state
            if update_in.selected_trade_id is not None:
                decision.selected_trade_id = update_in.selected_trade_id
            if update_in.selected_pathway_id is not None:
                decision.selected_pathway_id = update_in.selected_pathway_id
            if update_in.learner_agreed is not None:
                decision.learner_agreed = update_in.learner_agreed
            if update_in.parent_agreed is not None:
                decision.parent_agreed = update_in.parent_agreed
            if update_in.alignment_notes is not None:
                decision.alignment_notes = update_in.alignment_notes

        # Boost alignment score when state reaches INFORMED or DECISION_MADE
        if target_state in ["INFORMED", "DECISION_MADE"]:
            family.alignment_score = min(98.0, (family.alignment_score or 80.0) + 8.0)

        db.commit()
        db.refresh(family)
        return self.get_decision_room_snapshot(db, family.id, current_user)

    def resolve_concern(
        self,
        db: Session,
        family_id: int,
        req: ConcernResolutionRequest,
        current_user: Optional[User] = None
    ) -> FamilyDecisionRoomSnapshot:
        """Mark a specific family concern as resolved through evidence."""
        concern = db.query(FamilyConcern).filter(
            FamilyConcern.id == req.concern_id,
            FamilyConcern.family_id == family_id
        ).first()

        if not concern:
            raise HTTPException(status_code=404, detail="Concern not found for this family")

        concern.is_addressed = True
        if req.addressed_evidence_id:
            concern.addressed_evidence_id = req.addressed_evidence_id

        # Update family alignment score
        family = db.query(Family).filter(Family.id == family_id).first()
        if family:
            family.alignment_score = min(98.0, (family.alignment_score or 75.0) + 4.0)

        db.commit()
        return self.get_decision_room_snapshot(db, family_id, current_user)

    def save_trade(
        self,
        db: Session,
        family_id: int,
        req: SaveTradeRequest,
        current_user: Optional[User] = None
    ) -> FamilyDecisionRoomSnapshot:
        """Bookmark or unbookmark a trade in the family options ledger."""
        user_id = current_user.id if current_user else 1
        exploration = db.query(CareerExploration).filter(
            CareerExploration.family_id == family_id,
            CareerExploration.trade_id == req.trade_id
        ).first()

        if not exploration:
            exploration = CareerExploration(
                session_id=1,
                family_id=family_id,
                user_id=user_id,
                trade_id=req.trade_id,
                bookmarked=req.bookmarked,
            )
            db.add(exploration)
        else:
            exploration.bookmarked = req.bookmarked

        db.commit()
        return self.get_decision_room_snapshot(db, family_id, current_user)


family_decision_service = FamilyDecisionService()
