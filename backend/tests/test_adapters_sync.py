"""
SkillSathi - Source Adapters and Sync Engine Tests
"""
import pytest
from app.data_sources.sync_engine import sync_engine
from app.models.trade import Trade, TradeCategory, TrainingProvider
from app.models.outcome import OutcomeData, EmploymentData, EarningsData
from app.models.evidence_source import EvidenceSource, DataSyncRun


@pytest.mark.asyncio
async def test_ncvet_nqr_adapter_sync(db_session):
    result = await sync_engine.sync_by_key("ncvet_nqr", db_session, triggered_by="TEST_RUNNER")
    assert result["status"] == "COMPLETED"
    assert result["records_found"] > 0
    assert result["records_inserted"] > 0
    assert result["records_rejected"] == 0

    # Verify trades created in database
    trades = db_session.query(Trade).all()
    assert len(trades) >= 4
    solar_trade = db_session.query(Trade).filter(Trade.code == "ELE/Q5901").first()
    assert solar_trade is not None
    assert solar_trade.nsqf_level == 4
    assert solar_trade.is_demo is False

    # Verify career pathways created
    assert len(solar_trade.career_pathways) > 0
    pathway = solar_trade.career_pathways[0]
    assert len(pathway.steps) >= 3


@pytest.mark.asyncio
async def test_msde_tracer_adapter_sync(db_session):
    # First sync qualifications so trades exist
    await sync_engine.sync_by_key("ncvet_nqr", db_session, triggered_by="TEST_RUNNER")

    # Sync tracer outcomes
    result = await sync_engine.sync_by_key("msde_tracer", db_session, triggered_by="TEST_RUNNER")
    assert result["status"] == "COMPLETED"
    assert result["records_inserted"] > 0

    # Verify outcomes created
    outcomes = db_session.query(OutcomeData).all()
    assert len(outcomes) >= 4

    # Check first outcome provenance
    outcome = outcomes[0]
    assert outcome.source_id is not None
    assert outcome.placement_rate > 0
    assert outcome.is_demo is False
    assert outcome.verification_status == "OFFICIAL_VERIFIED"

    # Verify source entity attributes
    source = db_session.query(EvidenceSource).filter(EvidenceSource.id == outcome.source_id).first()
    assert source is not None
    assert "MSDE" in source.source_name
    assert source.freshness_status == "FRESH"


@pytest.mark.asyncio
async def test_demo_seed_adapter_is_demo_flag(db_session):
    result = await sync_engine.sync_by_key("demo_seed", db_session, triggered_by="TEST_RUNNER")
    assert result["status"] == "COMPLETED"

    # Verify all records from demo seed have is_demo = True
    demo_trade = db_session.query(Trade).filter(Trade.code == "DEMO/AGRI/Q01").first()
    assert demo_trade is not None
    assert demo_trade.is_demo is True

    demo_outcome = db_session.query(OutcomeData).filter(OutcomeData.trade_id == demo_trade.id).first()
    assert demo_outcome is not None
    assert demo_outcome.is_demo is True
    assert demo_outcome.verification_status == "UNVERIFIED"
