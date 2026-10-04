"""
SkillSathi - Family Unit, User, Learner, Parent, Concern, and Decision Models
Treats the FAMILY as the fundamental decision unit for vocational education choices.
"""
import enum
from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    ForeignKey,
    Text,
    Boolean,
    Date,
    JSON,
    Index,
)
from sqlalchemy.orm import relationship
from app.models.base import TimeStampedBase


class FamilyRole(str, enum.Enum):
    LEARNER = "LEARNER"
    PARENT = "PARENT"
    GUARDIAN = "GUARDIAN"
    COUNSELLOR = "COUNSELLOR"
    ADMIN = "ADMIN"


class ConcernCategory(str, enum.Enum):
    INCOME = "INCOME"
    JOB_SECURITY = "JOB_SECURITY"
    SOCIAL_STATUS = "SOCIAL_STATUS"
    SAFETY = "SAFETY"
    CAREER_GROWTH = "CAREER_GROWTH"
    FURTHER_EDUCATION = "FURTHER_EDUCATION"
    LOCATION = "LOCATION"
    AFFORDABILITY = "AFFORDABILITY"
    OTHER = "OTHER"


class User(TimeStampedBase):
    __tablename__ = "users"

    full_name = Column(String(128), nullable=False)
    role = Column(String(32), default=FamilyRole.LEARNER.value, nullable=False, index=True)
    phone_number = Column(String(20), nullable=True, index=True)
    email = Column(String(128), unique=True, nullable=True, index=True)
    password_hash = Column(String(255), nullable=True)
    preferred_language = Column(String(16), default="en", nullable=False)
    avatar_url = Column(String(255), nullable=True)
    family_id = Column(Integer, ForeignKey("families.id", ondelete="SET NULL"), nullable=True, index=True)

    # Relationships
    family = relationship("Family", back_populates="members", foreign_keys=[family_id])
    learner_profile = relationship("Learner", back_populates="user", uselist=False, cascade="all, delete-orphan")
    parent_profile = relationship("ParentGuardian", back_populates="user", uselist=False, cascade="all, delete-orphan")
    concerns = relationship("FamilyConcern", back_populates="user", cascade="all, delete-orphan")
    counselling_messages = relationship("CounsellingMessage", back_populates="sender_user")
    admin_events = relationship("AdminEvent", back_populates="admin_user")


class Family(TimeStampedBase):
    __tablename__ = "families"

    family_code = Column(String(32), unique=True, index=True, nullable=False)
    family_name = Column(String(128), nullable=True)
    location_id = Column(Integer, ForeignKey("locations.id", ondelete="SET NULL"), nullable=True, index=True)
    state = Column(String(64), nullable=True, index=True)
    district = Column(String(64), nullable=True, index=True)
    household_income_bracket = Column(String(64), nullable=True)  # e.g., "< 2.5 LPA", "2.5 - 5 LPA"
    primary_language = Column(String(16), default="en", nullable=False)
    education_context = Column(String(128), nullable=True)        # e.g., "First Generation Vocational Aspirant"
    mobility_preference = Column(String(64), default="LOCAL_DISTRICT", nullable=False)
    family_priorities = Column(JSON, nullable=True)               # e.g., ["JOB_SECURITY", "INCOME", "SAFETY"]
    onboarding_status = Column(String(32), default="NOT_STARTED", nullable=False)  # NOT_STARTED, IN_PROGRESS, COMPLETED
    alignment_score = Column(Float, default=50.0, nullable=False)
    created_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships
    location = relationship("Location", back_populates="families")
    members = relationship("User", back_populates="family", foreign_keys="User.family_id")
    learners = relationship("Learner", back_populates="family", cascade="all, delete-orphan")
    parents = relationship("ParentGuardian", back_populates="family", cascade="all, delete-orphan")
    concerns = relationship("FamilyConcern", back_populates="family", cascade="all, delete-orphan")
    decisions = relationship("FamilyDecision", back_populates="family", cascade="all, delete-orphan")
    counselling_sessions = relationship("CounsellingSession", back_populates="family", cascade="all, delete-orphan")
    counsellor_cases = relationship("CounsellorCase", back_populates="family", cascade="all, delete-orphan")


class Learner(TimeStampedBase):
    __tablename__ = "learners"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    family_id = Column(Integer, ForeignKey("families.id", ondelete="CASCADE"), nullable=False, index=True)
    current_education_grade = Column(String(64), default="10th Standard", nullable=False)
    school_or_college = Column(String(192), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String(32), nullable=True)
    academic_strengths = Column(JSON, nullable=True)              # e.g. ["PRACTICAL_HANDS_ON", "SCIENCE_TECH"]
    interest_areas = Column(JSON, nullable=True)                  # e.g. ["SOLAR_ENERGY", "MACHINES_ENGINES"]
    skills_or_hobbies = Column(JSON, nullable=True)
    preferred_work_environment = Column(String(64), default="WORKSHOP", nullable=False)  # WORKSHOP, OFFICE, FIELD, CLINIC
    career_aspirations = Column(Text, nullable=True)
    location_preference = Column(String(64), default="NEAR_HOME", nullable=False)  # NEAR_HOME, WITHIN_STATE, METROS_ALLOWED
    expected_salary_monthly_inr = Column(Integer, default=20000, nullable=False)
    further_education_goals = Column(String(64), default="LATERAL_DEGREE", nullable=False)  # LATERAL_DEGREE, DIRECT_JOB, APPRENTICESHIP_STUDY
    onboarding_step = Column(Integer, default=1, nullable=False)
    is_onboarding_complete = Column(Boolean, default=False, nullable=False)

    # Relationships
    user = relationship("User", back_populates="learner_profile")
    family = relationship("Family", back_populates="learners")
    preferences = relationship("LearnerPreference", back_populates="learner", cascade="all, delete-orphan")


class ParentGuardian(TimeStampedBase):
    __tablename__ = "parents_guardians"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    family_id = Column(Integer, ForeignKey("families.id", ondelete="CASCADE"), nullable=False, index=True)
    relationship_type = Column(String(32), default="PARENT", nullable=False)  # FATHER, MOTHER, GUARDIAN, ELDER_SIBLING
    occupation = Column(String(128), nullable=True)
    monthly_household_income_inr = Column(Integer, nullable=True)
    top_priorities = Column(JSON, nullable=True)                  # e.g. ["INCOME", "JOB_SECURITY", "SAFETY", "SOCIAL_STATUS"]
    raw_concerns_text = Column(Text, nullable=True)
    onboarding_step = Column(Integer, default=1, nullable=False)
    is_onboarding_complete = Column(Boolean, default=False, nullable=False)

    # Relationships
    user = relationship("User", back_populates="parent_profile")
    family = relationship("Family", back_populates="parents")


class FamilyConcern(TimeStampedBase):
    __tablename__ = "family_concerns"

    family_id = Column(Integer, ForeignKey("families.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    source_role = Column(String(32), default="PARENT", nullable=False)
    category = Column(String(64), default="GENERAL", nullable=False, index=True)
    concern_text = Column(Text, nullable=False)
    severity_level = Column(Integer, default=5, nullable=False)   # 1 to 10 scale
    confidence_score = Column(Float, default=0.85, nullable=False) # AI mapping confidence
    concern_type = Column(String(32), default="reported concern", nullable=False) # "detected concern" or "reported concern"
    is_addressed = Column(Boolean, default=False, nullable=False)
    addressed_evidence_id = Column(Integer, ForeignKey("outcome_data.id", ondelete="SET NULL"), nullable=True)

    # Relationships
    family = relationship("Family", back_populates="concerns")
    user = relationship("User", back_populates="concerns")


class LearnerPreference(TimeStampedBase):
    __tablename__ = "learner_preferences"

    learner_id = Column(Integer, ForeignKey("learners.id", ondelete="CASCADE"), nullable=False, index=True)
    preferred_trade_id = Column(Integer, ForeignKey("trades.id", ondelete="SET NULL"), nullable=True, index=True)
    interest_tags = Column(String(256), nullable=True)
    willing_to_relocate = Column(Boolean, default=False, nullable=False)
    preferred_work_environment = Column(String(64), default="WORKSHOP", nullable=False)

    # Relationships
    learner = relationship("Learner", back_populates="preferences")


class FamilyDecision(TimeStampedBase):
    __tablename__ = "family_decisions"

    family_id = Column(Integer, ForeignKey("families.id", ondelete="CASCADE"), nullable=False, index=True)
    selected_trade_id = Column(Integer, ForeignKey("trades.id", ondelete="SET NULL"), nullable=True, index=True)
    selected_pathway_id = Column(Integer, ForeignKey("career_pathways.id", ondelete="SET NULL"), nullable=True)
    decision_status = Column(String(64), default="EXPLORING", nullable=False, index=True)  # EXPLORING, ALIGNED, DISAGREEMENT, ESCALATED_TO_HUMAN, FINALIZED
    learner_agreed = Column(Boolean, default=False, nullable=False)
    parent_agreed = Column(Boolean, default=False, nullable=False)
    alignment_notes = Column(Text, nullable=True)

    # Relationships
    family = relationship("Family", back_populates="decisions")
