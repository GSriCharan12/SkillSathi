"""
SkillSathi - Comprehensive End-to-End (E2E) Journey Test
Smart India Hackathon 2026 - Problem Statement 26241:
"AI-Enabled Career Counselling and Family Decision-Support Platform for Vocational Education"

Full Journey Scenario:
1. Onboarding & Registration (Learner Aarav + Parent Sunita in Warangal)
2. Parental Concern Ingestion (Job Security & Starting Salary Certainty)
3. Career Exploration & DGT Verified Evidence Retrieval (Solar PV Specialist)
4. AI Grounded Counselling with Anti-Hallucination Constraints
5. Career Pathway & Lateral Degree Ladder Exploration
6. Family Decision Room Multi-Perspective Synchronization
7. Human Counsellor Escalation Ticket Creation
8. Counsellor Claims Case, Adds Shared Family Guidance Notes, and Recommends PMKVY Scheme
9. Scheme Administrator Dashboard Telemetry Updates & Anonymized CSV Export
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.family import Family, User, Learner, ParentGuardian, FamilyConcern, FamilyRole, FamilyDecision
from app.models.trade import Trade, TradeCategory, TrainingProvider
from app.models.outcome import OutcomeData, EarningsData, EmploymentData
from app.models.evidence_source import EvidenceSource
from app.models.pathway import CareerPathway, CareerPathwayStep
from app.models.counselling import CounsellingSession, CounsellorCase, CounsellorNote


def test_complete_sih_user_journey(client: TestClient, db_session: Session):
    # -------------------------------------------------------------
    # STAGE 1: Data Ground Truth Seeding (Verified Government Sources)
    # -------------------------------------------------------------
    source = EvidenceSource(
        source_name="NCVET & DGT Vocational Tracer Study 2024",
        publisher="Directorate General of Training (MSDE)",
        url="https://dgt.gov.in/tracer-studies-2024",
        source_type="GOVERNMENT_PORTAL",
        verification_status="OFFICIAL_VERIFIED",
        freshness_status="FRESH",
        geographic_scope="TELANGANA",
        is_demo=False,
    )
    cat = TradeCategory(code="RENEWABLE_ENERGY", name="Renewable & Clean Energy", icon_name="Sun")
    db_session.add_all([source, cat])
    db_session.flush()

    trade = Trade(
        category_id=cat.id,
        code="SOLAR_TECH_01",
        title="Solar PV & Clean Energy Technician",
        sector="Green Jobs",
        nsqf_level=4,
        duration_months=24,
        min_qualification="10th Class Pass",
        description="Comprehensive hands-on training in solar panel installation and industrial power wiring.",
        is_demo=False,
    )
    db_session.add(trade)
    db_session.flush()

    outcome = OutcomeData(
        trade_id=trade.id,
        source_id=source.id,
        placement_rate=86.5,
        earnings_min=18000,
        earnings_max=28000,
        employment_type="FORMAL_SECTOR",
        data_year=2024,
        verification_status="OFFICIAL_VERIFIED",
        is_demo=False,
    )
    earnings = EarningsData(
        trade_id=trade.id,
        source_id=source.id,
        median_starting_monthly_inr=19500,
        mid_career_monthly_inr=42000,
        stipend_during_training_inr=3000,
        is_demo=False,
    )
    employment = EmploymentData(
        trade_id=trade.id,
        source_id=source.id,
        formal_contract_pct=88.0,
        retention_rate_1yr=84.0,
        top_hiring_sectors=["Renewable Energy", "Power Distribution"],
        top_employer_names=["Tata Power Solar", "Adani Solar", "Telangana State Renewable Energy Corp"],
        is_demo=False,
    )
    pathway = CareerPathway(
        trade_id=trade.id,
        title="Solar Technician to Renewable Project Lead Ladder",
        entry_qualification="10th Class",
        total_progression_years=6,
        is_demo=False,
    )
    db_session.add_all([outcome, earnings, employment, pathway])
    db_session.flush()

    step1 = CareerPathwayStep(
        pathway_id=pathway.id,
        step_order=1,
        role_title="Junior Solar Installer",
        experience_required_months=0,
        expected_monthly_inr_min=18000,
        expected_monthly_inr_max=22000,
        education_ladder_option="AICTE Direct 2nd Year Lateral Polytechnic Entry Eligible",
    )
    step2 = CareerPathwayStep(
        pathway_id=pathway.id,
        step_order=2,
        role_title="Senior Solar Grid Technician",
        experience_required_months=24,
        expected_monthly_inr_min=28000,
        expected_monthly_inr_max=38000,
        education_ladder_option="B.Voc Lateral Degree Entry Eligible",
    )
    db_session.add_all([step1, step2])
    db_session.flush()

    # -------------------------------------------------------------
    # STAGE 2: Family Registration & Onboarding
    # -------------------------------------------------------------
    family = Family(
        family_code="SK-JOURNEY-99",
        family_name="Sharma Family Room",
        state="Telangana",
        district="Warangal",
        alignment_score=75.0,
    )
    counsellor_user = User(
        full_name="Dr. V. Sharma (Certified Counsellor)",
        role=FamilyRole.COUNSELLOR.value,
        phone_number="+91 98765 00000",
        email="counsellor.sharma@skillsathi.gov.in",
    )
    db_session.add_all([family, counsellor_user])
    db_session.flush()

    learner_user = User(
        full_name="Aarav Sharma",
        role=FamilyRole.LEARNER.value,
        family_id=family.id,
    )
    parent_user = User(
        full_name="Sunita Sharma (Mother)",
        role=FamilyRole.PARENT.value,
        family_id=family.id,
    )
    db_session.add_all([learner_user, parent_user])
    db_session.flush()

    learner_profile = Learner(
        user_id=learner_user.id,
        family_id=family.id,
        current_education_grade="10th Standard",
        interest_areas=["Solar PV", "Electrical Systems"],
        expected_salary_monthly_inr=20000,
        further_education_goals="LATERAL_DEGREE",
        is_onboarding_complete=True,
    )
    parent_profile = ParentGuardian(
        user_id=parent_user.id,
        family_id=family.id,
        relationship_type="MOTHER",
        top_priorities=["JOB_SECURITY", "INCOME", "FURTHER_EDUCATION"],
        raw_concerns_text="Worried about starting salary stability and whether lateral degree options exist.",
        is_onboarding_complete=True,
    )
    concern = FamilyConcern(
        family_id=family.id,
        user_id=parent_user.id,
        source_role="PARENT",
        category="JOB_SECURITY",
        concern_text="Is starting job secure with formal PF/ESI in Warangal?",
        severity_level=8,
        is_addressed=False,
    )
    decision = FamilyDecision(
        family_id=family.id,
        selected_trade_id=trade.id,
        decision_status="EXPLORING",
    )
    db_session.add_all([learner_profile, parent_profile, concern, decision])
    db_session.commit()

    # -------------------------------------------------------------
    # STAGE 3: Career Exploration & Verified Detail Lookup
    # -------------------------------------------------------------
    trades_res = client.get(f"/api/v1/trades/{trade.id}")
    assert trades_res.status_code == 200
    trade_detail = trades_res.json()["data"]
    assert trade_detail["title"] == "Solar PV & Clean Energy Technician"
    assert trade_detail["nsqf_level"] == 4

    outcomes_res = client.get(f"/api/v1/outcomes?trade_id={trade.id}")
    assert outcomes_res.status_code == 200
    outcomes_list = outcomes_res.json()["data"]
    assert len(outcomes_list) >= 1
    assert outcomes_list[0]["placement_rate"] == 86.5

    # -------------------------------------------------------------
    # STAGE 4: AI Vocational Grounded Counselling Dialogue
    # -------------------------------------------------------------
    counselling_msg_res = client.post("/api/v1/counselling/message", json={
        "message": "Will my child have job security and a formal salary after studying Solar PV?",
        "speaker_role": "PARENT",
        "trade_id": trade.id,
        "language": "en",
    })
    assert counselling_msg_res.status_code == 200
    ai_response = counselling_msg_res.json()["data"]
    assert ai_response["detected_intent"] in ["JOB_SECURITY", "INCOME", "CAREER_GROWTH"]
    assert ai_response["is_evidence_available"] is True
    assert len(ai_response["evidence_citations"]) >= 1
    session_id = ai_response["session_id"]

    # -------------------------------------------------------------
    # STAGE 5: Family Decision Room Perspective Snapshot
    # -------------------------------------------------------------
    decision_room_res = client.get(f"/api/v1/family-decisions/{family.id}")
    assert decision_room_res.status_code == 200
    decision_data = decision_room_res.json()["data"]
    assert decision_data["family_code"] == "SK-JOURNEY-99"
    assert decision_data["learner_perspective"]["name"] == "Aarav Sharma"
    assert decision_data["parent_perspective"]["name"] == "Sunita Sharma (Mother)"
    assert decision_data["decision_status"] == "EXPLORING"

    # Move decision state to DISCUSSING
    state_update_res = client.patch(f"/api/v1/family-decisions/{family.id}/state", json={
        "decision_status": "DISCUSSING",
        "selected_trade_id": trade.id,
        "alignment_notes": "Reviewing formal contract percentages together.",
    })
    assert state_update_res.status_code == 200
    assert state_update_res.json()["data"]["decision_status"] == "DISCUSSING"

    # Resolve concern
    resolve_res = client.post(f"/api/v1/family-decisions/{family.id}/resolve-concern", json={
        "concern_id": concern.id,
    })
    assert resolve_res.status_code == 200
    assert resolve_res.json()["data"]["resolved_concerns_count"] >= 1

    # -------------------------------------------------------------
    # STAGE 6: Human Counsellor Escalation Ticket Creation
    # -------------------------------------------------------------
    escalate_res = client.post("/api/v1/counsellor-cases", json={
        "family_id": family.id,
        "learner_id": learner_profile.id,
        "trade_id": trade.id,
        "priority": "HIGH",
        "escalation_reason": "Family requesting 1-on-1 verification of lateral B.Tech pathway.",
        "preferred_contact_method": "PHONE_CALL",
        "contact_details": "+91 98765 11111",
    })
    assert escalate_res.status_code == 201
    case_out = escalate_res.json()["data"]
    case_id = case_out["id"]
    assert case_out["case_status"] == "OPEN"

    # -------------------------------------------------------------
    # STAGE 7: Counsellor Claims Case, Adds Note, Recommends Resource
    # -------------------------------------------------------------
    assign_res = client.post(f"/api/v1/counsellor-cases/{case_id}/assign", json={
        "counsellor_id": counsellor_user.id,
    })
    assert assign_res.status_code == 200
    assert assign_res.json()["data"]["case_status"] == "ASSIGNED"

    note_res = client.post(f"/api/v1/counsellor-cases/{case_id}/notes", json={
        "note_text": "Verified with AICTE 2024 guidelines: Direct 2nd-year lateral entry to Polytechnic is confirmed.",
        "visibility": "FAMILY_SHARED",
        "is_action_item": True,
    })
    assert note_res.status_code == 200

    resource_res = client.post(f"/api/v1/counsellor-cases/{case_id}/resources", json={
        "resource_type": "SCHEME",
        "title": "Telangana State ITI Hostel & Fee Subsidy",
        "description": "100% tuition waiver with ₹3,000 monthly maintenance stipend.",
        "url": "https://iti.telangana.gov.in/schemes",
    })
    assert resource_res.status_code == 200

    resolve_case_res = client.patch(f"/api/v1/counsellor-cases/{case_id}/status", json={
        "case_status": "RESOLVED",
        "resolution_summary": "Family agreed on Solar PV trade after lateral degree confirmation.",
    })
    assert resolve_case_res.status_code == 200
    assert resolve_case_res.json()["data"]["case_status"] == "RESOLVED"

    # Move Family Decision state to DECISION_MADE
    final_decision_res = client.patch(f"/api/v1/family-decisions/{family.id}/state", json={
        "decision_status": "DECISION_MADE",
        "learner_agreed": True,
        "parent_agreed": True,
        "alignment_notes": "Joint consensus reached on Solar PV & Clean Energy Technician.",
    })
    assert final_decision_res.status_code == 200
    assert final_decision_res.json()["data"]["decision_status"] == "DECISION_MADE"

    # -------------------------------------------------------------
    # STAGE 8: Scheme Administrator Telemetry & Export
    # -------------------------------------------------------------
    admin_res = client.get("/api/v1/admin/analytics/programme?district=Warangal")
    assert admin_res.status_code == 200
    admin_data = admin_res.json()["data"]
    assert admin_data["overview"]["families_counselled"] >= 1
    assert len(admin_data["resistance_index"]) >= 1

    csv_res = client.get("/api/v1/admin/analytics/export")
    assert csv_res.status_code == 200
    assert "Family_Code" in csv_res.text
    # Privacy check: No learner names in CSV
    assert "Aarav Sharma" not in csv_res.text
