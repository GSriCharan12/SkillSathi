"""
SkillSathi - AI Counselling Service
Coordinates multi-lingual dialogue, family context, concern detection,
ranked evidence retrieval, LLM generation, and human escalation.
Strict Anti-Hallucination Policy: Zero fabricated statistics.
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session, joinedload

from app.models.counselling import CounsellingSession, CounsellingMessage, CareerExploration, CounsellorCase
from app.models.family import Family, User, Learner, ParentGuardian
from app.models.trade import Trade
from app.ai.factory import AIProviderFactory
from app.ai.language_detector import LanguageDetector
from app.ai.intent_detector import IntentDetector
from app.ai.counselling_strategy import CounsellingStrategyEngine
from app.services.concern_engine import ConcernEngine
from app.services.evidence_retrieval_service import EvidenceRetrievalService
from app.services.family_service import FamilyService
from app.utils.logger import logger


class CounsellingService:
    @staticmethod
    def get_or_create_session(
        db: Session,
        family_id: int,
        session_type: str = "JOINT_FAMILY_ROOM"
    ) -> CounsellingSession:
        active_sess = db.query(CounsellingSession).filter(
            CounsellingSession.family_id == family_id,
            CounsellingSession.completed_at.is_(None)
        ).order_by(CounsellingSession.created_at.desc()).first()

        if not active_sess:
            active_sess = CounsellingSession(
                family_id=family_id,
                session_type=session_type,
                current_stage="CONCERN_DISCOVERY",
                alignment_score=85.0
            )
            db.add(active_sess)
            db.commit()
            db.refresh(active_sess)

        return active_sess

    @staticmethod
    async def process_dialogue_turn(
        db: Session,
        user_message: str,
        user_role: str = "PARENT",
        user_id: Optional[int] = None,
        family_id: Optional[int] = None,
        session_id: Optional[int] = None,
        active_trade_id: Optional[int] = None,
        locale: str = "en-IN"
    ) -> Dict[str, Any]:
        """
        Executes the complete 8-step AI Counselling Pipeline.
        """
        # 1. Resolve Family & Session
        if not family_id and user_id:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                family_id = user.family_id

        if not family_id:
            # Resolve or fallback to demo family
            family = db.query(Family).first()
            if family:
                family_id = family.id
            else:
                family = Family(
                    family_code="SK-DEMO-01",
                    family_name="Demo Family",
                    state="Telangana",
                    district="Warangal",
                    is_active=True
                )
                db.add(family)
                db.commit()
                db.refresh(family)
                family_id = family.id

        if not session_id:
            session = CounsellingService.get_or_create_session(db, family_id=family_id)
            session_id = session.id
        else:
            session = db.query(CounsellingSession).filter(CounsellingSession.id == session_id).first()
            if not session:
                session = CounsellingService.get_or_create_session(db, family_id=family_id)
                session_id = session.id

        # 2. Step 1: Language Detection
        lang_info = LanguageDetector.detect_language(user_message)

        # 3. Step 2: Intent Detection
        intent_info = IntentDetector.detect_intent(user_message)
        intent = intent_info["primary_intent"]

        # 4. Step 3: Family Context Retrieval
        family_snapshot = FamilyService.get_family_snapshot(db, family_id)
        learner_data = family_snapshot.get("learner") or {}
        parent_data = family_snapshot.get("parent") or {}

        # Resolve active trade
        trade_title = "Solar PV Project Technician"
        trade_code = "ELE/Q5901"
        if active_trade_id:
            t_obj = db.query(Trade).filter(Trade.id == active_trade_id).first()
            if t_obj:
                trade_title = t_obj.title
                trade_code = t_obj.code
        else:
            # Pick first available trade in database
            first_t = db.query(Trade).first()
            if first_t:
                active_trade_id = first_t.id
                trade_title = first_t.title
                trade_code = first_t.code

        family_context = {
            "family_id": family_id,
            "family_code": family_snapshot.get("family_code"),
            "district": family_snapshot.get("district", "Warangal"),
            "state": family_snapshot.get("state", "Telangana"),
            "user_role": user_role,
            "learner_name": learner_data.get("name", "Aarav"),
            "learner_grade": learner_data.get("grade", "10th Standard"),
            "learner_strengths": learner_data.get("interests", []),
            "parent_priorities": parent_data.get("priorities", ["JOB_SECURITY", "INCOME", "FURTHER_EDUCATION"]),
            "alignment_score": family_snapshot.get("alignment_score", 88.0),
            "active_trade_id": active_trade_id,
            "active_trade_title": trade_title,
            "active_trade_code": trade_code
        }

        # 5. Step 4: Concern Analysis
        detected_concerns = ConcernEngine.map_concerns_from_text(user_message, source_role=user_role)

        # 6. Step 5: Ranked Evidence Retrieval
        evidence_result = EvidenceRetrievalService.retrieve_ranked_evidence(
            db=db,
            trade_id=active_trade_id,
            trade_code=trade_code,
            state=family_context["state"],
            district=family_context["district"],
            concern_type=intent if intent in ["INCOME", "JOB_SECURITY", "FURTHER_EDUCATION", "SAFETY", "LOCAL_AVAILABILITY"] else None,
            query=user_message,
            limit=5
        )

        available_evidence = evidence_result.get("items", [])
        is_evidence_available = evidence_result.get("is_available", False)

        # 7. Step 6: Strategy Formulation
        strategy = CounsellingStrategyEngine.determine_strategy(
            intent=intent,
            detected_concerns=detected_concerns,
            family_context=family_context,
            available_evidence=available_evidence,
            is_evidence_available=is_evidence_available,
            language_info=lang_info
        )

        # 8. Step 7: LLM Generation via AI Provider
        provider = AIProviderFactory.get_provider()
        ai_response = await provider.generate_counselling_response(
            user_message=user_message,
            family_context=family_context,
            detected_concerns=detected_concerns,
            available_evidence=available_evidence,
            locale=lang_info.get("locale", "en-IN")
        )

        # 9. Step 8: Persist Messages in Session Memory
        # A. User message
        user_msg_record = CounsellingMessage(
            session_id=session_id,
            sender_user_id=user_id,
            sender_role=user_role,
            message_text=user_message,
            detected_concerns=[c["category"] for c in detected_concerns] if detected_concerns else [intent],
            cited_evidence_ids=[]
        )
        db.add(user_msg_record)

        # B. AI Counsellor message
        ai_msg_record = CounsellingMessage(
            session_id=session_id,
            sender_user_id=None,
            sender_role="AI_COUNSELLOR",
            message_text=ai_response.content,
            detected_concerns=ai_response.detected_concerns,
            cited_evidence_ids=ai_response.recommended_evidence_ids
        )
        db.add(ai_msg_record)
        db.commit()
        db.refresh(ai_msg_record)

        # Filter and prepare full evidence cards to return to UI
        cited_evidence_cards = []
        if available_evidence:
            cited_evidence_cards = available_evidence[:2]

        is_evidence_available = len(available_evidence) > 0

        return {
            "message_id": ai_msg_record.id,
            "session_id": session_id,
            "speaker_role": "AI_COUNSELLOR",
            "content": ai_response.content,
            "detected_intent": intent,
            "detected_concerns": ai_response.detected_concerns,
            "language_detected": lang_info,
            "is_evidence_available": is_evidence_available,
            "cited_evidence": cited_evidence_cards,
            "evidence_citations": cited_evidence_cards,
            "suggested_chips": ai_response.suggested_questions,
            "family_context": family_context,
            "should_escalate_to_human": strategy["should_escalate_to_human"],
            "escalation_reason": strategy["escalation_reason"],
            "created_at": ai_msg_record.created_at.isoformat() if ai_msg_record.created_at else datetime.now(timezone.utc).isoformat()
        }

    @staticmethod
    def escalate_to_human_counsellor(
        db: Session,
        family_id: int,
        reason: str,
        priority: str = "HIGH"
    ) -> Dict[str, Any]:
        case = CounsellorCase(
            family_id=family_id,
            priority=priority,
            case_status="PENDING",
            escalation_reason=reason,
            counsellor_notes="Automated case generation via SkillSathi decision escalation."
        )
        db.add(case)
        db.commit()
        db.refresh(case)

        return {
            "case_id": case.id,
            "family_id": case.family_id,
            "priority": case.priority,
            "case_status": case.case_status,
            "escalation_reason": case.escalation_reason,
            "estimated_call_time": "Within 24 business hours",
            "message": "A certified vocational counsellor will review your family priorities and connect with you."
        }

    @staticmethod
    def get_session_history(db: Session, session_id: int) -> List[Dict[str, Any]]:
        messages = db.query(CounsellingMessage).filter(
            CounsellingMessage.session_id == session_id
        ).order_by(CounsellingMessage.created_at.asc()).all()

        results = []
        for m in messages:
            results.append({
                "id": m.id,
                "session_id": m.session_id,
                "sender_role": m.sender_role,
                "sender_user_id": m.sender_user_id,
                "message_text": m.message_text,
                "detected_concerns": m.detected_concerns or [],
                "cited_evidence_ids": m.cited_evidence_ids or [],
                "created_at": m.created_at.isoformat() if m.created_at else None
            })
        return results
