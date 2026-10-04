"""
SkillSathi - Family, User, Onboarding, and Family Snapshot Schemas
"""
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from pydantic import Field, EmailStr
from app.schemas.common import BaseSchema, TimestampedSchema
from app.models.family import FamilyRole, ConcernCategory


# 1. Authentication Schemas
class UserRegisterRequest(BaseSchema):
    full_name: str
    email: Optional[str] = None
    phone_number: Optional[str] = None
    password: str = Field(..., min_length=6)
    role: FamilyRole = FamilyRole.LEARNER
    preferred_language: str = "en"
    family_code: Optional[str] = None  # To join existing family or create new if null


class UserLoginRequest(BaseSchema):
    email_or_phone: str
    password: str
    role: Optional[FamilyRole] = None



class UserRead(TimestampedSchema):
    full_name: str
    role: str
    phone_number: Optional[str] = None
    email: Optional[str] = None
    preferred_language: str = "en"
    avatar_url: Optional[str] = None
    family_id: Optional[int] = None


class TokenResponse(BaseSchema):
    access_token: str
    token_type: str = "bearer"
    user: UserRead
    family_code: Optional[str] = None
    family_id: Optional[int] = None


# 2. Learner Onboarding Schemas
class LearnerOnboardingUpdate(BaseSchema):
    current_education_grade: Optional[str] = "10th Standard"
    school_or_college: Optional[str] = None
    gender: Optional[str] = None
    academic_strengths: Optional[List[str]] = []
    interest_areas: Optional[List[str]] = []
    skills_or_hobbies: Optional[List[str]] = []
    preferred_work_environment: Optional[str] = "WORKSHOP"
    career_aspirations: Optional[str] = None
    location_preference: Optional[str] = "NEAR_HOME"
    expected_salary_monthly_inr: Optional[int] = 20000
    further_education_goals: Optional[str] = "LATERAL_DEGREE"
    onboarding_step: Optional[int] = 1
    is_complete: Optional[bool] = False


class LearnerRead(TimestampedSchema):
    user_id: int
    family_id: int
    current_education_grade: str
    school_or_college: Optional[str] = None
    academic_strengths: Optional[List[str]] = []
    interest_areas: Optional[List[str]] = []
    skills_or_hobbies: Optional[List[str]] = []
    preferred_work_environment: str
    career_aspirations: Optional[str] = None
    location_preference: str
    expected_salary_monthly_inr: int
    further_education_goals: str
    onboarding_step: int
    is_onboarding_complete: bool


# 3. Parent Onboarding Schemas
class ParentOnboardingUpdate(BaseSchema):
    relationship_type: Optional[str] = "PARENT"
    occupation: Optional[str] = None
    monthly_household_income_inr: Optional[int] = None
    top_priorities: Optional[List[str]] = []
    raw_concerns_text: Optional[str] = None
    onboarding_step: Optional[int] = 1
    is_complete: Optional[bool] = False


class ParentRead(TimestampedSchema):
    user_id: int
    family_id: int
    relationship_type: str
    occupation: Optional[str] = None
    monthly_household_income_inr: Optional[int] = None
    top_priorities: Optional[List[str]] = []
    raw_concerns_text: Optional[str] = None
    onboarding_step: int
    is_onboarding_complete: bool


# 4. Family Concern Schemas
class FamilyConcernRead(TimestampedSchema):
    family_id: int
    user_id: int
    source_role: str
    category: str
    concern_text: str
    severity_level: int
    confidence_score: float
    concern_type: str
    is_addressed: bool
    addressed_evidence_id: Optional[int] = None


# 5. Family Snapshot & Alignment Schemas
class FamilySnapshotResponse(BaseSchema):
    family_id: int
    family_code: str
    family_name: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    education_context: Optional[str] = None
    household_income_bracket: Optional[str] = None
    onboarding_status: str
    alignment_score: float
    learner: Optional[Dict[str, Any]] = None
    parent: Optional[Dict[str, Any]] = None
    shared_priorities: List[str] = []
    different_priorities: List[str] = []
    detected_concerns: List[FamilyConcernRead] = []
    recommended_discussion_points: List[str] = []
