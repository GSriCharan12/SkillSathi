"""
SkillSathi - Family Experience, Authentication, and Onboarding Automated Tests
Tests registration, login, learner onboarding, parent onboarding, concern extraction, and family snapshot.
"""
import pytest
from app.services.family_service import FamilyService
from app.services.concern_engine import ConcernEngine
from app.schemas.family import (
    UserRegisterRequest,
    UserLoginRequest,
    LearnerOnboardingUpdate,
    ParentOnboardingUpdate,
)
from app.models.family import FamilyRole, Family, Learner, ParentGuardian, FamilyConcern


def test_concern_engine_extraction():
    # 1. Income concern
    concerns = ConcernEngine.analyze_natural_language_concern(
        "I am very worried about low salary and whether the starting income will be enough."
    )
    assert len(concerns) >= 1
    assert concerns[0]["category"] == "INCOME"
    assert concerns[0]["severity_level"] >= 7
    assert concerns[0]["concern_type"] == "detected concern"

    # 2. Safety & Status concern
    multi_concerns = ConcernEngine.analyze_natural_language_concern(
        "Is this workplace safe for girls and what will relatives say about social respect?"
    )
    categories = [c["category"] for c in multi_concerns]
    assert "SAFETY" in categories
    assert "SOCIAL_STATUS" in categories


@pytest.mark.asyncio
async def test_auth_and_family_onboarding_journey(client, db_session):
    # 1. Register Learner (Creates new family)
    learner_reg = UserRegisterRequest(
        full_name="Aarav Sharma",
        email="aarav@skillsathi.test",
        password="SecurePassword123!",
        role=FamilyRole.LEARNER,
        preferred_language="en"
    )
    reg_res = client.post("/api/v1/auth/register", json=learner_reg.model_dump())
    assert reg_res.status_code == 200
    learner_auth = reg_res.json()["data"]
    learner_token = learner_auth["access_token"]
    family_code = learner_auth["family_code"]
    family_id = learner_auth["family_id"]
    assert family_code.startswith("SK-")

    # 2. Learner Onboarding (Step 1 -> Step 6)
    learner_headers = {"Authorization": f"Bearer {learner_token}"}
    learner_update = LearnerOnboardingUpdate(
        current_education_grade="10th Standard",
        school_or_college="Model High School",
        academic_strengths=["PRACTICAL_HANDS_ON", "SCIENCE_TECH"],
        interest_areas=["SOLAR_ENERGY", "MACHINES_ENGINES"],
        skills_or_hobbies=["Circuit Assembling"],
        preferred_work_environment="WORKSHOP",
        career_aspirations="Solar PV Project Engineer",
        location_preference="NEAR_HOME",
        expected_salary_monthly_inr=22000,
        further_education_goals="LATERAL_DEGREE",
        onboarding_step=6,
        is_complete=True
    )
    lo_res = client.post("/api/v1/family/learner/onboarding", headers=learner_headers, json=learner_update.model_dump())
    assert lo_res.status_code == 200
    assert lo_res.json()["data"]["is_onboarding_complete"] is True

    # 3. Register Parent joining the SAME Family Code
    parent_reg = UserRegisterRequest(
        full_name="Sunita Sharma",
        email="sunita@skillsathi.test",
        password="ParentPassword123!",
        role=FamilyRole.PARENT,
        preferred_language="en",
        family_code=family_code  # Joins Aarav's room
    )
    preg_res = client.post("/api/v1/auth/register", json=parent_reg.model_dump())
    assert preg_res.status_code == 200
    parent_auth = preg_res.json()["data"]
    parent_token = parent_auth["access_token"]
    assert parent_auth["family_id"] == family_id

    # 4. Parent Onboarding & Natural Language Concern Capture
    parent_headers = {"Authorization": f"Bearer {parent_token}"}
    parent_update = ParentOnboardingUpdate(
        relationship_type="MOTHER",
        occupation="Homemaker / Small Business",
        monthly_household_income_inr=28000,
        top_priorities=["JOB_SECURITY", "INCOME", "FURTHER_EDUCATION", "SAFETY"],
        raw_concerns_text="I am worried about low starting salary and whether he can still complete a college degree.",
        onboarding_step=3,
        is_complete=True
    )
    po_res = client.post("/api/v1/family/parent/onboarding", headers=parent_headers, json=parent_update.model_dump())
    assert po_res.status_code == 200
    assert po_res.json()["data"]["is_onboarding_complete"] is True

    # 5. Retrieve Combined Family Snapshot
    snap_res = client.get(f"/api/v1/family/{family_id}/snapshot")
    assert snap_res.status_code == 200
    snap_data = snap_res.json()["data"]
    assert snap_data["family_code"] == family_code
    assert snap_data["onboarding_status"] == "COMPLETED"
    assert snap_data["learner"]["name"] == "Aarav Sharma"
    assert snap_data["parent"]["name"] == "Sunita Sharma"
    assert len(snap_data["shared_priorities"]) > 0
    assert len(snap_data["detected_concerns"]) >= 1
    assert snap_data["alignment_score"] > 0
