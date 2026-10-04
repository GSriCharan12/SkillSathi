"""
SkillSathi - AI Counselling Engine Tests
Validates multi-lingual dialogue turns (English, Telugu, Hinglish),
intent and concern detection, family context integration, evidence grounding,
zero-hallucination missing-data handling, and human counsellor escalation.
"""
import pytest
from app.data_sources.sync_engine import sync_engine


@pytest.mark.asyncio
async def test_counselling_dialogue_english_parent_concern(client, db_session):
    await sync_engine.sync_all(db_session, triggered_by="TEST_COUNSELLING")

    payload = {
        "user_message": "Will my child have job security and a good starting salary if they do Solar PV technician?",
        "user_role": "PARENT",
        "locale": "en-IN"
    }

    res = client.post("/api/v1/counselling/message", json=payload)
    assert res.status_code == 200
    data = res.json()["data"]

    assert data["speaker_role"] == "AI_COUNSELLOR"
    assert data["detected_intent"] in ["JOB_SECURITY", "INCOME", "CAREER_GROWTH"]
    assert "₹" in data["content"] or "placement" in data["content"].lower()
    assert len(data["suggested_chips"]) >= 2
    assert len(data["cited_evidence"]) >= 1


@pytest.mark.asyncio
async def test_counselling_dialogue_salary_and_outcomes_query(client, db_session):
    await sync_engine.sync_all(db_session, triggered_by="TEST_COUNSELLING")

    payload = {
        "user_message": "What is the expected starting salary and placement rate for an ITI solar technician?",
        "user_role": "PARENT",
        "locale": "en"
    }

    res = client.post("/api/v1/counselling/message", json=payload)
    assert res.status_code == 200
    data = res.json()["data"]

    assert data["speaker_role"] == "AI_COUNSELLOR"
    assert data["language_detected"]["primary_language"] in ["en", "english"]
    assert len(data["content"]) > 20
    assert any(w in data["content"].lower() for w in ["salary", "stipend", "placement", "₹", "solar", "rate"])



@pytest.mark.asyncio
async def test_counselling_dialogue_hinglish_further_education(client, db_session):
    await sync_engine.sync_all(db_session, triggered_by="TEST_COUNSELLING")

    payload = {
        "user_message": "Kya ITI ke baad aage college degree ya B.Tech mil sakti hai bina entrance exam ke?",
        "user_role": "PARENT",
        "locale": "hi-IN"
    }

    res = client.post("/api/v1/counselling/message", json=payload)
    assert res.status_code == 200
    data = res.json()["data"]

    assert data["speaker_role"] == "AI_COUNSELLOR"
    assert data["detected_intent"] == "FURTHER_EDUCATION"
    assert "lateral entry" in data["content"].lower() or "b.voc" in data["content"].lower() or "degree" in data["content"].lower()


@pytest.mark.asyncio
async def test_missing_evidence_anti_hallucination_safe_response(client, db_session):
    await sync_engine.sync_all(db_session, triggered_by="TEST_COUNSELLING")

    # Ask about a trade ID that doesn't exist
    payload = {
        "user_message": "What is the exact starting salary for Quantum Aerospace Nanotech technician?",
        "user_role": "LEARNER",
        "active_trade_id": 99999,
        "locale": "en-IN"
    }

    res = client.post("/api/v1/counselling/message", json=payload)
    assert res.status_code == 200
    data = res.json()["data"]

    assert "unavailable" in data["content"].lower()
    assert "anti-hallucination" in data["content"].lower() or "unverified" in data["content"].lower()


@pytest.mark.asyncio
async def test_human_counsellor_escalation(client, db_session):
    # 1. Escalate case directly
    payload = {
        "family_id": 1,
        "reason": "Parent and student have strong divergence on distant relocation and starting wage security.",
        "priority": "HIGH"
    }

    res = client.post("/api/v1/counselling/escalate", json=payload)
    assert res.status_code == 200
    data = res.json()["data"]

    assert data["case_status"] == "PENDING"
    assert data["priority"] == "HIGH"
    assert "counsellor" in data["message"].lower()


@pytest.mark.asyncio
async def test_suggested_starters_endpoint(client, db_session):
    res = client.get("/api/v1/counselling/suggested-prompts?role=PARENT&district=Warangal")
    assert res.status_code == 200
    prompts = res.json()["data"]["prompts"]
    assert len(prompts) >= 4
    assert any("Warangal" in p for p in prompts)
