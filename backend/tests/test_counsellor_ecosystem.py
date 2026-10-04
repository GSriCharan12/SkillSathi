"""
SkillSathi - Test Suite for Human Counsellor Ecosystem & Family Decision Room
Smart India Hackathon 2026 - Problem Statement 26241
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.family import Family, User, Learner, ParentGuardian, FamilyConcern, FamilyRole
from app.models.trade import Trade, TradeCategory
from app.models.counselling import CounsellorCase, CounsellorNote


@pytest.fixture
def setup_ecosystem_data(db_session: Session):
    """Seed test data for family, counsellor, trade, and initial concerns."""
    # 1. Create Counsellor User
    counsellor = User(
        full_name="Dr. V. Sharma (Certified Counsellor)",
        role=FamilyRole.COUNSELLOR.value,
        phone_number="+91 9988776655",
        email="counsellor@skillsathi.gov.in",
        preferred_language="en",
    )
    # 2. Create Family & Learner & Parent
    family = Family(
        family_code="SK-ECO-100",
        family_name="Reddy Family Room",
        state="Telangana",
        district="Warangal",
        alignment_score=78.0,
    )
    db_session.add_all([counsellor, family])
    db_session.flush()

    learner_user = User(
        full_name="Sai Kumar Reddy",
        role=FamilyRole.LEARNER.value,
        family_id=family.id,
    )
    parent_user = User(
        full_name="Venkatesh Reddy (Father)",
        role=FamilyRole.PARENT.value,
        family_id=family.id,
    )
    db_session.add_all([learner_user, parent_user])
    db_session.flush()

    learner = Learner(
        user_id=learner_user.id,
        family_id=family.id,
        current_education_grade="10th Standard",
        interest_areas=["Solar Energy", "Industrial Electricals"],
        expected_salary_monthly_inr=22000,
        is_onboarding_complete=True,
    )
    parent = ParentGuardian(
        user_id=parent_user.id,
        family_id=family.id,
        relationship_type="FATHER",
        top_priorities=["JOB_SECURITY", "INCOME", "FURTHER_EDUCATION"],
        raw_concerns_text="Starting salary must be secure and higher education should not be blocked.",
        is_onboarding_complete=True,
    )
    concern1 = FamilyConcern(
        family_id=family.id,
        user_id=parent_user.id,
        source_role="PARENT",
        category="JOB_SECURITY",
        concern_text="Is there formal contract guarantee and PF/ESI in solar technician jobs?",
        severity_level=7,
        confidence_score=0.92,
        is_addressed=False,
    )
    concern2 = FamilyConcern(
        family_id=family.id,
        user_id=parent_user.id,
        source_role="PARENT",
        category="FURTHER_EDUCATION",
        concern_text="Can he study B.Tech laterally without losing years?",
        severity_level=6,
        confidence_score=0.95,
        is_addressed=False,
    )

    category = TradeCategory(code="ENG_TECH", name="Engineering & Technical", icon_name="Zap")
    db_session.add(category)
    db_session.flush()

    trade = Trade(
        category_id=category.id,
        code="ELEC-01",
        title="Solar PV & Electrician Specialist",
        sector="Renewable Energy",
        nsqf_level=4,
        duration_months=24,
        min_qualification="10th Class Pass",
        description="Comprehensive training in solar PV installation and industrial wiring.",
    )

    db_session.add_all([learner, parent, concern1, concern2, trade])
    db_session.commit()

    return {
        "counsellor": counsellor,
        "family": family,
        "learner": learner,
        "parent": parent,
        "trade": trade,
        "concern1": concern1,
    }


def test_create_and_list_counsellor_case(client: TestClient, setup_ecosystem_data):
    data = setup_ecosystem_data
    # 1. Create human counsellor escalation case
    payload = {
        "family_id": data["family"].id,
        "learner_id": data["learner"].id,
        "trade_id": data["trade"].id,
        "priority": "HIGH",
        "escalation_reason": "Parent worried about starting salary stability and lateral degree admission.",
        "parent_concerns": ["Job security and PF/ESI formal status", "Lateral B.Tech admission eligibility"],
        "preferred_contact_method": "PHONE_CALL",
        "contact_details": "+91 98765 43210",
    }
    res = client.post("/api/v1/counsellor-cases", json=payload)
    assert res.status_code == 201
    json_data = res.json()
    assert json_data["success"] is True
    case = json_data["data"]
    assert case["case_status"] == "OPEN"
    assert case["priority"] == "HIGH"
    assert case["trade_title"] == "Solar PV & Electrician Specialist"

    case_id = case["id"]

    # 2. List cases
    list_res = client.get("/api/v1/counsellor-cases")
    assert list_res.status_code == 200
    cases_list = list_res.json()["data"]
    assert any(c["id"] == case_id for c in cases_list)


def test_case_assignment_and_status_progression(client: TestClient, setup_ecosystem_data):
    data = setup_ecosystem_data
    # Create case
    create_res = client.post("/api/v1/counsellor-cases", json={
        "family_id": data["family"].id,
        "trade_id": data["trade"].id,
        "priority": "URGENT",
        "escalation_reason": "Family requesting urgent 1-on-1 discussion on trade selection.",
    })
    case_id = create_res.json()["data"]["id"]

    # 1. Assign to counsellor
    assign_res = client.post(f"/api/v1/counsellor-cases/{case_id}/assign", json={
        "counsellor_id": data["counsellor"].id,
    })
    assert assign_res.status_code == 200
    assert assign_res.json()["data"]["case_status"] == "ASSIGNED"
    assert assign_res.json()["data"]["assigned_counsellor_id"] == data["counsellor"].id

    # 2. Update status to IN_PROGRESS
    status_res1 = client.patch(f"/api/v1/counsellor-cases/{case_id}/status", json={
        "case_status": "IN_PROGRESS",
    })
    assert status_res1.status_code == 200
    assert status_res1.json()["data"]["case_status"] == "IN_PROGRESS"

    # 3. Add private note and family shared note
    note1 = client.post(f"/api/v1/counsellor-cases/{case_id}/notes", json={
        "note_text": "Father is apprehensive due to first-generation vocational path. Verified NCVET tracer shown.",
        "visibility": "COUNSELLOR_PRIVATE",
        "is_action_item": False,
    })
    assert note1.status_code == 200

    note2 = client.post(f"/api/v1/counsellor-cases/{case_id}/notes", json={
        "note_text": "Next Step: Review Warangal Govt ITI hostel facilities and lateral B.Voc admission list.",
        "visibility": "FAMILY_SHARED",
        "is_action_item": True,
    })
    assert note2.status_code == 200

    # 4. Recommend resource
    res_rec = client.post(f"/api/v1/counsellor-cases/{case_id}/resources", json={
        "resource_type": "SCHEME",
        "title": "PMKVY 4.0 Special Stipend & Hostel Subsidy",
        "description": "Full fee waiver and ₹2,500 monthly stipend for certified NSQF Level 4 trades in Telangana.",
        "url": "https://skillsathi.gov.in/schemes/pmkvy-telangana",
    })
    assert res_rec.status_code == 200
    assert len(res_rec.json()["data"]["recommended_resources"]) > 0

    # 5. Resolve case
    resolve_res = client.patch(f"/api/v1/counsellor-cases/{case_id}/status", json={
        "case_status": "RESOLVED",
        "resolution_summary": "Family agreed on Solar PV trade after reviewing AICTE lateral degree roadmap and hostel subsidy.",
    })
    assert resolve_res.status_code == 200
    assert resolve_res.json()["data"]["case_status"] == "RESOLVED"
    assert resolve_res.json()["data"]["resolved_at"] is not None


def test_counsellor_dashboard_summary(client: TestClient, setup_ecosystem_data):
    res = client.get("/api/v1/counsellor-cases/dashboard-summary")
    assert res.status_code == 200
    summary = res.json()["data"]
    assert "total_cases" in summary
    assert "new_cases" in summary
    assert "active_cases" in summary
    assert "resolved_cases" in summary


def test_family_decision_room_snapshot_and_state_updates(client: TestClient, setup_ecosystem_data):
    data = setup_ecosystem_data
    family_id = data["family"].id

    # 1. Fetch Decision Room Snapshot
    snap_res = client.get(f"/api/v1/family-decisions/{family_id}")
    assert snap_res.status_code == 200
    snapshot = snap_res.json()["data"]
    assert snapshot["family_code"] == "SK-ECO-100"
    assert snapshot["decision_status"] in ["EXPLORING", "DISCUSSING"]
    assert "learner_perspective" in snapshot
    assert "parent_perspective" in snapshot
    assert len(snapshot["reported_concerns"]) >= 2

    # 2. Update state to DISCUSSING with selected trade
    state_res1 = client.patch(f"/api/v1/family-decisions/{family_id}/state", json={
        "decision_status": "DISCUSSING",
        "selected_trade_id": data["trade"].id,
        "learner_agreed": True,
        "parent_agreed": False,
        "alignment_notes": "Father exploring salary progression records.",
    })
    assert state_res1.status_code == 200
    assert state_res1.json()["data"]["decision_status"] == "DISCUSSING"

    # 3. Resolve a concern
    resolve_concern_res = client.post(f"/api/v1/family-decisions/{family_id}/resolve-concern", json={
        "concern_id": data["concern1"].id,
        "resolution_notes": "NCVET 2024 data verified 88% formal contract rate.",
    })
    assert resolve_concern_res.status_code == 200
    assert resolve_concern_res.json()["data"]["resolved_concerns_count"] >= 1

    # 4. Save trade in options ledger
    save_trade_res = client.post(f"/api/v1/family-decisions/{family_id}/save-trade", json={
        "trade_id": data["trade"].id,
        "bookmarked": True,
    })
    assert save_trade_res.status_code == 200

    # 5. Move state to INFORMED and DECISION_MADE
    state_res2 = client.patch(f"/api/v1/family-decisions/{family_id}/state", json={
        "decision_status": "INFORMED",
        "selected_trade_id": data["trade"].id,
        "learner_agreed": True,
        "parent_agreed": True,
        "alignment_notes": "Both learner and parent reviewed evidence and aligned on next steps.",
    })
    assert state_res2.status_code == 200
    assert state_res2.json()["data"]["decision_status"] == "INFORMED"
    assert state_res2.json()["data"]["alignment_score"] >= 78.0


def test_live_case_presence(client: TestClient, setup_ecosystem_data):
    res = client.get("/api/v1/counsellor-cases/1/presence")
    assert res.status_code == 200
    presence = res.json()["data"]
    assert "is_connected" in presence
    assert "counsellor_online" in presence
    assert "family_online" in presence
