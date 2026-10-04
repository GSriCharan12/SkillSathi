"""
SkillSathi - Test Suite for Administrator and Programme Analytics System
Smart India Hackathon 2026 - Problem Statement 26241:
"A dashboard for scheme administrators showing where and why family resistance is concentrated."
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.family import Family, User, Learner, ParentGuardian, FamilyConcern, FamilyRole, FamilyDecision
from app.models.trade import Trade, TradeCategory
from app.models.counselling import CounsellorCase, CareerExploration, CounsellingSession


@pytest.fixture
def seed_analytics_data(db_session: Session):
    """Seeds multi-district families, trades, concerns, and cases for analytics verification."""
    # 1. Categories & Trades
    cat = TradeCategory(code="ENG_TECH", name="Engineering & Technical", icon_name="Zap")
    db_session.add(cat)
    db_session.flush()

    trade1 = Trade(
        category_id=cat.id,
        code="SOLAR_PV_01",
        title="Solar PV Specialist",
        sector="Renewable Energy",
        nsqf_level=4,
        duration_months=24,
        min_qualification="10th Pass",
    )
    trade2 = Trade(
        category_id=cat.id,
        code="CNC_MACH_02",
        title="CNC Precision Machinist",
        sector="Capital Goods",
        nsqf_level=5,
        duration_months=24,
        min_qualification="10th Pass with Science",
    )
    db_session.add_all([trade1, trade2])
    db_session.flush()

    # 2. Families in different districts (Warangal, Medchal, Hyderabad)
    f1 = Family(family_code="SK-WRG-01", family_name="Warangal Family 1", state="Telangana", district="Warangal", alignment_score=82.0)
    f2 = Family(family_code="SK-MCL-02", family_name="Medchal Family 2", state="Telangana", district="Medchal", alignment_score=68.0)
    f3 = Family(family_code="SK-HYD-03", family_name="Hyderabad Family 3", state="Telangana", district="Hyderabad", alignment_score=90.0)
    db_session.add_all([f1, f2, f3])
    db_session.flush()

    u1 = User(full_name="Student 1", role=FamilyRole.LEARNER.value, family_id=f1.id)
    u2 = User(full_name="Student 2", role=FamilyRole.LEARNER.value, family_id=f2.id)
    u3 = User(full_name="Student 3", role=FamilyRole.LEARNER.value, family_id=f3.id)
    db_session.add_all([u1, u2, u3])
    db_session.flush()

    # 3. Reported concerns with various severities and categories
    c1 = FamilyConcern(family_id=f1.id, user_id=u1.id, source_role="PARENT", category="JOB_SECURITY", concern_text="Need formal contract proof", severity_level=8, is_addressed=False)
    c2 = FamilyConcern(family_id=f1.id, user_id=u1.id, source_role="PARENT", category="INCOME", concern_text="Starting wage parity concern", severity_level=7, is_addressed=False)
    c3 = FamilyConcern(family_id=f2.id, user_id=u2.id, source_role="PARENT", category="SOCIAL_STATUS", concern_text="Neighbourhood perception", severity_level=9, is_addressed=False)
    c4 = FamilyConcern(family_id=f3.id, user_id=u3.id, source_role="PARENT", category="FURTHER_EDUCATION", concern_text="Lateral B.Tech entry", severity_level=5, is_addressed=True)

    # 4. Decisions
    d1 = FamilyDecision(family_id=f1.id, selected_trade_id=trade1.id, decision_status="DISCUSSING")
    d2 = FamilyDecision(family_id=f2.id, selected_trade_id=trade2.id, decision_status="NEEDS_COUNSELLING")
    d3 = FamilyDecision(family_id=f3.id, selected_trade_id=trade1.id, decision_status="INFORMED", learner_agreed=True, parent_agreed=True)

    # 5. Escalations & Explorations
    case1 = CounsellorCase(family_id=f2.id, trade_id=trade2.id, priority="HIGH", case_status="OPEN", escalation_reason="High family perception resistance.")
    exp1 = CareerExploration(session_id=1, family_id=f1.id, user_id=u1.id, trade_id=trade1.id, bookmarked=True)
    exp2 = CareerExploration(session_id=1, family_id=f2.id, user_id=u2.id, trade_id=trade2.id, bookmarked=True)

    db_session.add_all([c1, c2, c3, c4, d1, d2, d3, case1, exp1, exp2])
    db_session.commit()

    return {
        "trades": [trade1, trade2],
        "families": [f1, f2, f3],
        "concerns": [c1, c2, c3, c4],
        "case": case1,
    }


def test_programme_analytics_overview(client: TestClient, seed_analytics_data):
    res = client.get("/api/v1/admin/analytics/programme")
    assert res.status_code == 200
    json_data = res.json()
    assert json_data["success"] is True
    data = json_data["data"]

    # 1. Overview metrics
    overview = data["overview"]
    assert overview["families_counselled"] >= 3
    assert overview["total_trades_cataloged"] >= 2
    assert overview["counsellor_escalations"] >= 1
    assert overview["average_family_alignment"] > 0

    # 2. Transparent Resistance Indicator
    resistance_items = data["resistance_index"]
    assert len(resistance_items) >= 3
    for r in resistance_items:
        assert 0.0 <= r["concern_score"] <= 100.0
        assert r["resistance_level"] in ["LOW", "MODERATE", "HIGH", "ACUTE"]
        assert r["decision_state"] is not None

    # Verify resistance methodology documentation is present
    assert "Family Concern/Resistance Index" in data["resistance_methodology"]


def test_concern_analytics_breakdown(client: TestClient, seed_analytics_data):
    res = client.get("/api/v1/admin/analytics/concerns")
    assert res.status_code == 200
    concerns = res.json()["data"]
    assert len(concerns) >= 8  # 8 categories
    categories = [c["category"] for c in concerns]
    assert "INCOME" in categories
    assert "JOB_SECURITY" in categories
    assert "SOCIAL_STATUS" in categories
    assert "FURTHER_EDUCATION" in categories


def test_geographic_hotspot_analytics(client: TestClient, seed_analytics_data):
    res = client.get("/api/v1/admin/analytics/geographic")
    assert res.status_code == 200
    hotspots = res.json()["data"]
    assert len(hotspots) >= 1
    districts = [h["district"] for h in hotspots]
    assert any(d in districts for d in ["Warangal", "Medchal", "Hyderabad"])


def test_trade_analytics_and_counselling_funnel(client: TestClient, seed_analytics_data):
    # 1. Trade Analytics
    t_res = client.get("/api/v1/admin/analytics/trades")
    assert t_res.status_code == 200
    trades = t_res.json()["data"]
    assert len(trades) >= 2
    assert any(t["trade_title"] == "Solar PV Specialist" for t in trades)

    # 2. Counselling Funnel
    f_res = client.get("/api/v1/admin/analytics/funnel")
    assert f_res.status_code == 200
    funnel = f_res.json()["data"]
    assert len(funnel) == 7
    stage_keys = [st["stage_key"] for st in funnel]
    assert "STARTED" in stage_keys
    assert "CONCERN_IDENTIFIED" in stage_keys
    assert "EVIDENCE_VIEWED" in stage_keys
    assert "DECISION_COMPLETED" in stage_keys
    assert "COUNSELLOR_ESCALATED" in stage_keys


def test_anonymized_csv_export(client: TestClient, seed_analytics_data):
    res = client.get("/api/v1/admin/analytics/export")
    assert res.status_code == 200
    assert "text/csv" in res.headers["content-type"]
    csv_text = res.text
    assert "Family_Code" in csv_text
    assert "Resistance_Score" in csv_text
    assert "Resistance_Level" in csv_text
    # Ensure privacy: NO personal names or phone numbers appear
    assert "Student 1" not in csv_text
    assert "+91" not in csv_text


def test_programme_analytics_geographic_filtering(client: TestClient, seed_analytics_data):
    res = client.get("/api/v1/admin/analytics/programme?district=Warangal")
    assert res.status_code == 200
    data = res.json()["data"]
    # All resistance index records should match Warangal filter
    for item in data["resistance_index"]:
        assert item["district"] == "Warangal"
