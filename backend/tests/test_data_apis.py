"""
SkillSathi - Real Data API Endpoints Integration Tests
Tests /api/v1/trades, /api/v1/providers, /api/v1/outcomes, /api/v1/pathways, /api/v1/evidence, /api/v1/admin/monitoring.
"""
import pytest
from app.data_sources.sync_engine import sync_engine


@pytest.mark.asyncio
async def test_trades_api_flow(client, db_session):
    # Seed data
    await sync_engine.sync_all(db_session, triggered_by="API_TEST")

    # 1. GET /api/v1/trades
    res = client.get("/api/v1/trades")
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert len(data["data"]) >= 4

    # 2. Search filter
    search_res = client.get("/api/v1/trades?search=Solar")
    assert search_res.status_code == 200
    solar_items = search_res.json()["data"]
    assert len(solar_items) >= 1
    assert "Solar" in solar_items[0]["title"]

    # 3. Sector filter
    sector_res = client.get("/api/v1/trades?sector=Automotive")
    assert sector_res.status_code == 200
    auto_items = sector_res.json()["data"]
    assert len(auto_items) >= 1

    # 4. Detail endpoint /trades/{id}
    trade_id = solar_items[0]["id"]
    detail_res = client.get(f"/api/v1/trades/{trade_id}")
    assert detail_res.status_code == 200
    detail_data = detail_res.json()["data"]
    assert detail_data["id"] == trade_id
    assert len(detail_data["career_pathways"]) > 0


@pytest.mark.asyncio
async def test_providers_api(client, db_session):
    await sync_engine.sync_all(db_session, triggered_by="API_TEST")

    res = client.get("/api/v1/providers")
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert len(data["data"]) >= 4

    # State filter
    mh_res = client.get("/api/v1/providers?state=Maharashtra")
    assert mh_res.status_code == 200
    mh_data = mh_res.json()["data"]
    assert len(mh_data) >= 1


@pytest.mark.asyncio
async def test_outcomes_api_and_provenance(client, db_session):
    await sync_engine.sync_all(db_session, triggered_by="API_TEST")

    res = client.get("/api/v1/outcomes")
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert len(data["data"]) >= 4

    # Check that provenance is fully attached
    first_outcome = data["data"][0]
    assert first_outcome["placement_rate"] > 0
    assert first_outcome["source"] is not None
    assert first_outcome["source"]["source_name"] != ""


@pytest.mark.asyncio
async def test_pathways_api(client, db_session):
    await sync_engine.sync_all(db_session, triggered_by="API_TEST")

    res = client.get("/api/v1/pathways")
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert len(data["data"]) >= 4
    first_pathway = data["data"][0]
    assert len(first_pathway["steps"]) > 0


@pytest.mark.asyncio
async def test_evidence_and_monitoring_api(client, db_session):
    await sync_engine.sync_all(db_session, triggered_by="API_TEST")

    # 1. Evidence list
    res_ev = client.get("/api/v1/evidence")
    assert res_ev.status_code == 200
    ev_data = res_ev.json()["data"]
    assert len(ev_data) >= 3

    # 2. Admin monitoring telemetry
    res_mon = client.get("/api/v1/admin/monitoring")
    assert res_mon.status_code == 200
    mon_data = res_mon.json()["data"]
    assert mon_data["total_sources"] >= 3
    assert mon_data["total_trades"] >= 4
    assert mon_data["total_outcomes"] >= 4
    assert mon_data["total_sync_runs"] >= 3


@pytest.mark.asyncio
async def test_data_sync_router_endpoints(client, db_session):
    # 1. List registered adapters
    res_adapters = client.get("/api/v1/data-sync/adapters")
    assert res_adapters.status_code == 200
    assert len(res_adapters.json()["data"]) >= 3

    # 2. Trigger all sync via API
    res_sync = client.post("/api/v1/data-sync/trigger-all")
    assert res_sync.status_code == 200
    assert res_sync.json()["success"] is True
