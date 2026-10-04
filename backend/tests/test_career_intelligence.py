"""
SkillSathi - Vocational Career Intelligence Layer Tests
Validates Career Explorer, Localized Prioritization (Telangana/Warangal),
Interactive Pathways, Multi-Pathway Comparisons, Ranked Evidence Retrieval,
Strict Missing-Data Safeguards, and Freshness Audits.
"""
import pytest
from app.data_sources.sync_engine import sync_engine
from app.services.trade_service import TradeService
from app.services.evidence_retrieval_service import EvidenceRetrievalService


@pytest.mark.asyncio
async def test_localized_career_explorer_prioritization(client, db_session):
    # Ingest seed datasets
    await sync_engine.sync_all(db_session, triggered_by="TEST_INTEL")

    # 1. Request trades localized to Warangal, Telangana
    res = client.get("/api/v1/trades?state=Telangana&district=Warangal")
    assert res.status_code == 200
    payload = res.json()
    assert payload["success"] is True
    trades = payload["data"]
    assert len(trades) >= 4

    # Trades with local providers in Warangal (e.g., Solar PV, Agri-Drone) should be prioritized first
    top_trade = trades[0]
    assert top_trade["has_local_availability"] is True
    assert top_trade["local_provider_count"] > 0
    assert top_trade["verified_placement_rate"] is not None

    # Verify freshness string
    assert "Verified data" in top_trade["freshness_label"]


@pytest.mark.asyncio
async def test_trade_dossier_and_complete_pathway_ladder(client, db_session):
    await sync_engine.sync_all(db_session, triggered_by="TEST_INTEL")

    # Find Solar PV trade
    search_res = client.get("/api/v1/trades?search=Solar")
    solar_id = search_res.json()["data"][0]["id"]

    # Get trade detail dossier
    dossier_res = client.get(f"/api/v1/trades/{solar_id}?state=Telangana&district=Warangal")
    assert dossier_res.status_code == 200
    dossier = dossier_res.json()["data"]

    # Verify structural fields required by PS 26241
    assert dossier["title"] == "Solar PV Project Technician"
    assert dossier["nsqf_level"] == 4
    assert dossier["duration_months"] == 12
    assert dossier["min_qualification"] != ""
    assert dossier["verified_outcome"] is not None
    assert dossier["verified_outcome"]["placement_rate"] > 0
    assert dossier["verified_outcome"]["median_starting_monthly_inr"] > 0

    # Verify interactive pathway ladder nodes
    pathways = dossier["career_pathways"]
    assert len(pathways) >= 1
    steps = pathways[0]["steps"]
    assert len(steps) >= 3

    # Check step hierarchy: Entry role -> Experience / Progression -> Specialist / Degree
    assert steps[0]["step_order"] == 1
    assert steps[0]["role_title"] != ""
    assert steps[0]["experience_required_months"] == 0
    assert steps[0]["expected_monthly_inr_min"] is not None

    # Check lateral education progression option
    assert any(s.get("education_ladder_option") for s in steps)


@pytest.mark.asyncio
async def test_pathway_side_by_side_comparison(client, db_session):
    await sync_engine.sync_all(db_session, triggered_by="TEST_INTEL")

    all_trades = client.get("/api/v1/trades").json()["data"]
    trade_id_1 = all_trades[0]["id"]
    trade_id_2 = all_trades[1]["id"]

    # Compare 2 pathways in Warangal, Telangana
    comp_res = client.get(f"/api/v1/trades/compare?trade_ids={trade_id_1},{trade_id_2}&state=Telangana&district=Warangal")
    assert comp_res.status_code == 200
    comp_data = comp_res.json()["data"]

    assert comp_data["comparison_count"] == 2
    trades_matrix = comp_data["trades"]
    assert len(trades_matrix) == 2

    for t in trades_matrix:
        assert "trade_title" in t
        assert "nsqf_level" in t
        assert "duration_months" in t
        assert "local_availability" in t
        assert "career_progression_steps" in t
        assert "further_education_routes" in t
        assert "evidence_source" in t


@pytest.mark.asyncio
async def test_ranked_evidence_retrieval_service(client, db_session):
    await sync_engine.sync_all(db_session, triggered_by="TEST_INTEL")

    # 1. Retrieve evidence for Warangal Telangana
    ev_res = client.get("/api/v1/evidence/retrieve?state=Telangana&district=Warangal&concern_type=INCOME")
    assert ev_res.status_code == 200
    ev_payload = ev_res.json()["data"]

    assert ev_payload["is_available"] is True
    assert ev_payload["items_count"] > 0
    top_item = ev_payload["items"][0]

    # Verify evidence card attributes
    assert "claim" in top_item
    assert "value" in top_item
    assert "trade_title" in top_item
    assert "source_publisher" in top_item
    assert "verification_status" in top_item
    assert top_item["verification_status"] == "OFFICIAL_VERIFIED"
    assert top_item["relevance_score"] > 50


@pytest.mark.asyncio
async def test_strict_anti_hallucination_for_missing_evidence(client, db_session):
    await sync_engine.sync_all(db_session, triggered_by="TEST_INTEL")

    # Request evidence for a fictitious or nonexistent query with no matches
    res = client.get("/api/v1/evidence/retrieve?trade_id=99999&query=NonExistentQuantumAstronautics")
    assert res.status_code == 200
    payload = res.json()["data"]

    # Must return explicit unavailability message and zero hallucinated records
    assert payload["is_available"] is False
    assert payload["unavailability_message"] == "Verified information for this question is currently unavailable."
    assert payload["items_count"] == 0
    assert len(payload["items"]) == 0
