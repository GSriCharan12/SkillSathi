"""
SkillSathi - Family & Authentication Service
Manages user authentication, family unit creation, resumable onboarding, and family alignment calculation.
"""
import uuid
import secrets
from typing import Optional, Dict, Any, List, Tuple
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from app.models.family import (
    User,
    Family,
    Learner,
    ParentGuardian,
    FamilyConcern,
    FamilyRole,
    ConcernCategory,
)
from app.schemas.family import (
    UserRegisterRequest,
    UserLoginRequest,
    LearnerOnboardingUpdate,
    ParentOnboardingUpdate,
    FamilySnapshotResponse,
)
from app.security.auth import hash_password, verify_password, create_access_token
from app.services.concern_engine import ConcernEngine
from app.utils.logger import logger


class FamilyService:
    @staticmethod
    def generate_family_code() -> str:
        """Generate unique, easy-to-share family room code like 'SK-8492'."""
        num = secrets.randbelow(9000) + 1000
        return f"SK-{num}"

    @classmethod
    def register_user(cls, db: Session, req: UserRegisterRequest) -> Tuple[User, str, str]:
        """
        Registers user, creates or joins family, and returns (user, token, family_code).
        """
        # Check if email exists
        if req.email:
            existing = db.query(User).filter(User.email == req.email.strip().lower()).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"An account with email '{req.email}' already exists."
                )

        # 1. Resolve Family
        family = None
        if req.family_code:
            family = db.query(Family).filter(Family.family_code == req.family_code.strip().upper()).first()
            if not family:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Family Room with code '{req.family_code}' was not found."
                )
        else:
            # Create a new family unit
            family_code = cls.generate_family_code()
            family = Family(
                family_code=family_code,
                family_name=f"{req.full_name.split()[0]}'s Family",
                primary_language=req.preferred_language,
                onboarding_status="IN_PROGRESS",
                alignment_score=50.0
            )
            db.add(family)
            db.flush()

        # 2. Create User
        hashed = hash_password(req.password)
        user = User(
            full_name=req.full_name.strip(),
            email=req.email.strip().lower() if req.email else None,
            phone_number=req.phone_number.strip() if req.phone_number else None,
            password_hash=hashed,
            role=req.role.value if isinstance(req.role, FamilyRole) else req.role,
            preferred_language=req.preferred_language,
            family_id=family.id
        )
        db.add(user)
        db.flush()

        # 3. Create Corresponding Role Profile
        if user.role == FamilyRole.LEARNER.value:
            learner = Learner(user_id=user.id, family_id=family.id, onboarding_step=1)
            db.add(learner)
        elif user.role in (FamilyRole.PARENT.value, FamilyRole.GUARDIAN.value):
            parent = ParentGuardian(user_id=user.id, family_id=family.id, onboarding_step=1)
            db.add(parent)

        db.commit()
        db.refresh(user)
        db.refresh(family)

        token = create_access_token({"sub": str(user.id), "role": user.role, "family_id": family.id})
        return (user, token, family.family_code)

    @classmethod
    def authenticate_user(cls, db: Session, req: UserLoginRequest) -> Tuple[User, str, Optional[str]]:
        ident = req.email_or_phone.strip().lower()
        user = db.query(User).filter(
            (User.email == ident) | (User.phone_number == req.email_or_phone.strip())
        ).first()

        if not user or not verify_password(req.password, user.password_hash or ""):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email/phone or password."
            )

        # Enforce Strict Role Isolation (e.g. Student cannot login through Admin/Counsellor/Parent portal)
        if req.role is not None:
            expected_role_str = req.role.value if isinstance(req.role, FamilyRole) else str(req.role)
            user_role_str = user.role.value if isinstance(user.role, FamilyRole) else str(user.role)
            
            # Treat PARENT and GUARDIAN as compatible family portal roles
            roles_match = (
                user_role_str == expected_role_str
                or (user_role_str in ("PARENT", "GUARDIAN") and expected_role_str in ("PARENT", "GUARDIAN"))
            )
            if not roles_match:
                role_display_names = {
                    "LEARNER": "Student / Learner",
                    "PARENT": "Parent / Guardian",
                    "GUARDIAN": "Parent / Guardian",
                    "COUNSELLOR": "Certified Counsellor",
                    "ADMIN": "Scheme Administrator"
                }
                actual_name = role_display_names.get(user_role_str, user_role_str)
                attempted_name = role_display_names.get(expected_role_str, expected_role_str)
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Role mismatch: This account is registered as '{actual_name}'. You cannot sign in through the '{attempted_name}' portal. Please switch to the '{actual_name}' portal to log in."
                )

        family_code = user.family.family_code if user.family else None
        family_id = user.family_id
        token = create_access_token({"sub": str(user.id), "role": user.role, "family_id": family_id})
        return (user, token, family_code)


    @classmethod
    def update_learner_onboarding(
        cls,
        db: Session,
        user: User,
        data: LearnerOnboardingUpdate
    ) -> Learner:
        learner = db.query(Learner).filter(Learner.user_id == user.id).first()
        if not learner:
            learner = Learner(user_id=user.id, family_id=user.family_id)
            db.add(learner)
            db.flush()

        if data.current_education_grade is not None:
            learner.current_education_grade = data.current_education_grade
        if data.school_or_college is not None:
            learner.school_or_college = data.school_or_college
        if data.academic_strengths is not None:
            learner.academic_strengths = data.academic_strengths
        if data.interest_areas is not None:
            learner.interest_areas = data.interest_areas
        if data.skills_or_hobbies is not None:
            learner.skills_or_hobbies = data.skills_or_hobbies
        if data.preferred_work_environment is not None:
            learner.preferred_work_environment = data.preferred_work_environment
        if data.career_aspirations is not None:
            learner.career_aspirations = data.career_aspirations
        if data.location_preference is not None:
            learner.location_preference = data.location_preference
        if data.expected_salary_monthly_inr is not None:
            learner.expected_salary_monthly_inr = data.expected_salary_monthly_inr
        if data.further_education_goals is not None:
            learner.further_education_goals = data.further_education_goals
        if data.onboarding_step is not None:
            learner.onboarding_step = data.onboarding_step
        if data.is_complete is not None:
            learner.is_onboarding_complete = data.is_complete

        # Update family onboarding status if both completed
        cls._refresh_family_alignment(db, user.family_id)

        db.commit()
        db.refresh(learner)
        return learner

    @classmethod
    def update_parent_onboarding(
        cls,
        db: Session,
        user: User,
        data: ParentOnboardingUpdate
    ) -> ParentGuardian:
        parent = db.query(ParentGuardian).filter(ParentGuardian.user_id == user.id).first()
        if not parent:
            parent = ParentGuardian(user_id=user.id, family_id=user.family_id)
            db.add(parent)
            db.flush()

        if data.relationship_type is not None:
            parent.relationship_type = data.relationship_type
        if data.occupation is not None:
            parent.occupation = data.occupation
        if data.monthly_household_income_inr is not None:
            parent.monthly_household_income_inr = data.monthly_household_income_inr
        if data.top_priorities is not None:
            parent.top_priorities = data.top_priorities
        if data.onboarding_step is not None:
            parent.onboarding_step = data.onboarding_step
        if data.is_complete is not None:
            parent.is_onboarding_complete = data.is_complete

        # Process Natural Language Concerns if provided
        if data.raw_concerns_text and data.raw_concerns_text.strip():
            parent.raw_concerns_text = data.raw_concerns_text.strip()
            # Extract and persist mapped concerns
            extracted = ConcernEngine.analyze_natural_language_concern(
                text=data.raw_concerns_text,
                user_role="PARENT"
            )
            for conc in extracted:
                # Check duplicate
                existing_concern = db.query(FamilyConcern).filter(
                    FamilyConcern.family_id == user.family_id,
                    FamilyConcern.user_id == user.id,
                    FamilyConcern.category == conc["category"]
                ).first()

                if not existing_concern:
                    fc = FamilyConcern(
                        family_id=user.family_id,
                        user_id=user.id,
                        source_role="PARENT",
                        category=conc["category"],
                        concern_text=conc["concern_text"],
                        severity_level=conc["severity_level"],
                        confidence_score=conc["confidence_score"],
                        concern_type=conc["concern_type"]
                    )
                    db.add(fc)

        cls._refresh_family_alignment(db, user.family_id)

        db.commit()
        db.refresh(parent)
        return parent

    @classmethod
    def _refresh_family_alignment(cls, db: Session, family_id: Optional[int]):
        if not family_id:
            return
        family = db.query(Family).filter(Family.id == family_id).first()
        if not family:
            return

        learner = db.query(Learner).filter(Learner.family_id == family_id).first()
        parent = db.query(ParentGuardian).filter(ParentGuardian.family_id == family_id).first()
        concerns = db.query(FamilyConcern).filter(FamilyConcern.family_id == family_id).all()

        if learner and learner.is_onboarding_complete and parent and parent.is_onboarding_complete:
            family.onboarding_status = "COMPLETED"
        elif (learner and learner.is_onboarding_complete) or (parent and parent.is_onboarding_complete):
            family.onboarding_status = "IN_PROGRESS"

        # Calculate alignment score
        score = 80.0
        # Reduce score for unaddressed severe concerns
        for c in concerns:
            if not c.is_addressed and c.severity_level >= 7:
                score -= 8.0
            elif not c.is_addressed:
                score -= 3.0

        family.alignment_score = max(30.0, min(100.0, score))
        db.flush()

    @classmethod
    def get_family_snapshot(cls, db: Session, family_id: int) -> Dict[str, Any]:
        family = db.query(Family).options(
            joinedload(Family.learners).joinedload(Learner.user),
            joinedload(Family.parents).joinedload(ParentGuardian.user),
            joinedload(Family.concerns)
        ).filter(Family.id == family_id).first()

        if not family:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Family with ID {family_id} not found."
            )

        learner = family.learners[0] if family.learners else None
        parent = family.parents[0] if family.parents else None

        # Calculate Shared vs Differing priorities
        learner_strengths = set(learner.academic_strengths or []) if learner else set()
        learner_interests = set(learner.interest_areas or []) if learner else set()
        parent_priorities = set(parent.top_priorities or []) if parent else set()

        shared = []
        differing = []
        discussion_points = []

        if "INCOME" in parent_priorities or "JOB_SECURITY" in parent_priorities:
            if learner and learner.expected_salary_monthly_inr >= 20000:
                shared.append("Financial Stability & Earning Potential")
            else:
                differing.append("Starting Wage Expectations vs Industry Apprenticeships")
                discussion_points.append("Explore verified MSDE apprentice stipends and 1-year wage progression.")

        if "FURTHER_EDUCATION" in parent_priorities:
            if learner and learner.further_education_goals == "LATERAL_DEGREE":
                shared.append("Lateral Degree Mobility (B.Voc / Polytechnic to B.Tech)")
            else:
                discussion_points.append("Discuss AICTE/UGC recognized lateral degree pathways after ITI/Diploma.")

        if "SAFETY" in parent_priorities:
            discussion_points.append("Review certified industrial cluster safety ratings and commute proximity.")

        if not shared:
            shared = ["Career Growth & Modern Technical Qualification", "Building Family Prosperity"]

        return {
            "family_id": family.id,
            "family_code": family.family_code,
            "family_name": family.family_name,
            "state": family.state or "Maharashtra",
            "district": family.district or "Pune",
            "education_context": family.education_context or "First Generation Vocational Aspirant",
            "household_income_bracket": family.household_income_bracket or "2.5 - 5 Lakhs INR / Year",
            "onboarding_status": family.onboarding_status,
            "alignment_score": family.alignment_score,
            "learner": {
                "name": learner.user.full_name if learner and learner.user else "Learner",
                "grade": learner.current_education_grade if learner else "10th Standard",
                "interests": learner.interest_areas if learner else ["Solar Tech", "Mechatronics"],
                "work_env": learner.preferred_work_environment if learner else "WORKSHOP",
                "salary_goal": learner.expected_salary_monthly_inr if learner else 20000,
                "education_goal": learner.further_education_goals if learner else "LATERAL_DEGREE",
                "is_complete": learner.is_onboarding_complete if learner else False,
            } if learner else None,
            "parent": {
                "name": parent.user.full_name if parent and parent.user else "Parent/Guardian",
                "relationship": parent.relationship_type if parent else "PARENT",
                "priorities": parent.top_priorities if parent else ["JOB_SECURITY", "INCOME", "SAFETY"],
                "raw_concerns": parent.raw_concerns_text if parent else None,
                "is_complete": parent.is_onboarding_complete if parent else False,
            } if parent else None,
            "shared_priorities": shared,
            "different_priorities": differing,
            "detected_concerns": family.concerns,
            "recommended_discussion_points": discussion_points or [
                "Review verified 3-year salary progression verified by MSDE.",
                "Inspect lateral entry credit transfer to B.Voc degree programs."
            ],
        }
