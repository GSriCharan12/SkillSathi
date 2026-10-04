"""
SkillSathi - Demo User Accounts Seeder
Ensures standard demo accounts are always present in the database with role profiles and family association.
"""
from sqlalchemy.orm import Session
from app.models.family import User, Family, Learner, ParentGuardian, FamilyRole
from app.security.auth import hash_password
from app.utils.logger import logger


def seed_demo_users(db: Session):
    """Seed demo accounts if they do not exist."""
    demo_password_hash = hash_password("SecurePass123!")

    # 1. Ensure Demo Family Room SK-9482 exists
    family = db.query(Family).filter(Family.family_code == "SK-9482").first()
    if not family:
        family = Family(
            family_code="SK-9482",
            family_name="Sharma Family Room",
            state="Telangana",
            district="Warangal",
            household_income_bracket="2.5 - 5 LPA",
            primary_language="en",
            mobility_preference="LOCAL_DISTRICT",
            family_priorities=["JOB_SECURITY", "INCOME", "DEGREE_MOBILITY"],
            onboarding_status="IN_PROGRESS",
            alignment_score=78.5,
            is_active=True
        )
        db.add(family)
        db.flush()
        logger.info("Demo family unit 'SK-9482' created.")

    # 2. Demo User Definitions
    demo_accounts = [
        {
            "email": "parent.sharma@skillsathi.in",
            "full_name": "Ramesh Sharma",
            "phone_number": "9876543210",
            "role": FamilyRole.PARENT.value,
            "family_id": family.id,
            "profile_type": "PARENT",
        },
        {
            "email": "aarav.sharma@skillsathi.in",
            "full_name": "Aarav Sharma",
            "phone_number": "9876543211",
            "role": FamilyRole.LEARNER.value,
            "family_id": family.id,
            "profile_type": "LEARNER",
        },
        {
            "email": "counsellor.rao@skillsathi.in",
            "full_name": "Dr. S. Rao",
            "phone_number": "9876543212",
            "role": FamilyRole.COUNSELLOR.value,
            "family_id": None,
            "profile_type": None,
        },
        {
            "email": "admin.directorate@skillsathi.in",
            "full_name": "Directorate Admin",
            "phone_number": "9876543213",
            "role": FamilyRole.ADMIN.value,
            "family_id": None,
            "profile_type": None,
        },
    ]

    for acc in demo_accounts:
        user = db.query(User).filter(User.email == acc["email"]).first()
        if not user:
            user = User(
                email=acc["email"],
                full_name=acc["full_name"],
                phone_number=acc["phone_number"],
                role=acc["role"],
                password_hash=demo_password_hash,
                preferred_language="en",
                family_id=acc["family_id"],
            )
            db.add(user)
            db.flush()

            if acc["profile_type"] == "LEARNER":
                learner = Learner(
                    user_id=user.id,
                    family_id=family.id,
                    current_education_grade="10th Standard",
                    onboarding_step=3,
                    is_onboarding_complete=True,
                )
                db.add(learner)
            elif acc["profile_type"] == "PARENT":
                parent = ParentGuardian(
                    user_id=user.id,
                    family_id=family.id,
                    relationship_type="FATHER",
                    onboarding_step=3,
                    is_onboarding_complete=True,
                )
                db.add(parent)


            logger.info(f"Demo user '{acc['email']}' ({acc['role']}) seeded successfully.")
        else:
            # Update password hash in case it was modified
            user.password_hash = demo_password_hash
            user.role = acc["role"]
            if acc["family_id"]:
                user.family_id = acc["family_id"]

    db.commit()
