"""
SkillSathi - Counselling, Family Dialogue, Human Escalation, and Audit Models
"""
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, Text, JSON, Boolean, Index
from sqlalchemy.orm import relationship
from app.models.base import TimeStampedBase


class CounsellingSession(TimeStampedBase):
    __tablename__ = "counselling_sessions"

    family_id = Column(Integer, ForeignKey("families.id", ondelete="CASCADE"), nullable=False, index=True)
    session_type = Column(String(64), default="JOINT_FAMILY_ROOM", nullable=False, index=True)  # AI_FACILITATED, HUMAN_ESCALATED, JOINT_FAMILY_ROOM
    current_stage = Column(String(64), default="CONCERN_DISCOVERY", nullable=False)
    alignment_score = Column(Float, default=50.0, nullable=False)
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    family = relationship("Family", back_populates="counselling_sessions")
    messages = relationship("CounsellingMessage", back_populates="session", cascade="all, delete-orphan")
    explorations = relationship("CareerExploration", back_populates="session", cascade="all, delete-orphan")


class CounsellingMessage(TimeStampedBase):
    __tablename__ = "counselling_messages"

    session_id = Column(Integer, ForeignKey("counselling_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    sender_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    sender_role = Column(String(32), default="AI_COUNSELLOR", nullable=False, index=True)  # LEARNER, PARENT, AI_COUNSELLOR, HUMAN_COUNSELLOR
    message_text = Column(Text, nullable=False)
    detected_concerns = Column(JSON, nullable=True)
    cited_evidence_ids = Column(JSON, nullable=True)  # list of outcome_data ids

    # Relationships
    session = relationship("CounsellingSession", back_populates="messages")
    sender_user = relationship("User", back_populates="counselling_messages")


class CareerExploration(TimeStampedBase):
    __tablename__ = "career_explorations"

    session_id = Column(Integer, ForeignKey("counselling_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    family_id = Column(Integer, ForeignKey("families.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    trade_id = Column(Integer, ForeignKey("trades.id", ondelete="CASCADE"), nullable=False, index=True)
    view_duration_seconds = Column(Integer, default=0, nullable=False)
    bookmarked = Column(Boolean, default=False, nullable=False)

    # Relationships
    session = relationship("CounsellingSession", back_populates="explorations")


class CounsellorCase(TimeStampedBase):
    __tablename__ = "counsellor_cases"

    family_id = Column(Integer, ForeignKey("families.id", ondelete="CASCADE"), nullable=False, index=True)
    learner_id = Column(Integer, ForeignKey("learners.id", ondelete="SET NULL"), nullable=True, index=True)
    trade_id = Column(Integer, ForeignKey("trades.id", ondelete="SET NULL"), nullable=True, index=True)
    assigned_counsellor_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    
    priority = Column(String(32), default="MEDIUM", nullable=False, index=True)  # LOW, MEDIUM, HIGH, URGENT
    case_status = Column(String(32), default="OPEN", nullable=False, index=True)  # OPEN, ASSIGNED, IN_PROGRESS, RESOLVED, FOLLOW_UP_NEEDED
    
    escalation_reason = Column(Text, nullable=False)
    parent_concerns = Column(JSON, nullable=True)
    ai_summary = Column(Text, nullable=True)
    evidence_shown = Column(JSON, nullable=True)
    unresolved_questions = Column(JSON, nullable=True)
    recommended_resources = Column(JSON, nullable=True)
    resolution_summary = Column(Text, nullable=True)
    counsellor_notes = Column(Text, nullable=True)
    
    preferred_contact_method = Column(String(32), default="PHONE_CALL", nullable=False)
    contact_details = Column(String(128), nullable=True)
    scheduled_at = Column(DateTime, nullable=True)
    resolved_at = Column(DateTime, nullable=True)

    # Relationships
    family = relationship("Family", back_populates="counsellor_cases")
    assigned_counsellor = relationship("User", foreign_keys=[assigned_counsellor_id])
    learner = relationship("Learner", foreign_keys=[learner_id])
    trade = relationship("Trade", foreign_keys=[trade_id])
    notes = relationship("CounsellorNote", back_populates="case", cascade="all, delete-orphan", order_by="CounsellorNote.created_at.desc()")


class CounsellorNote(TimeStampedBase):
    __tablename__ = "counsellor_notes"

    case_id = Column(Integer, ForeignKey("counsellor_cases.id", ondelete="CASCADE"), nullable=False, index=True)
    author_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    note_text = Column(Text, nullable=False)
    visibility = Column(String(32), default="COUNSELLOR_PRIVATE", nullable=False)  # COUNSELLOR_PRIVATE, FAMILY_SHARED
    is_action_item = Column(Boolean, default=False, nullable=False)

    # Relationships
    case = relationship("CounsellorCase", back_populates="notes")
    author = relationship("User", foreign_keys=[author_id])


class AdminEvent(TimeStampedBase):
    __tablename__ = "admin_events"

    admin_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    action_type = Column(String(64), nullable=False, index=True)  # SYNC_TRIGGERED, DATA_OVERRIDE, USER_VERIFIED, EXPORT_REPORT
    entity_type = Column(String(64), nullable=False)
    entity_id = Column(String(64), nullable=True)
    details = Column(JSON, nullable=True)
    ip_address = Column(String(45), nullable=True)

    # Relationships
    admin_user = relationship("User", back_populates="admin_events")

