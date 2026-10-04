"""
SkillSathi - Health Endpoint Unit & Integration Tests
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_app_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["status"] == "healthy"
    assert data["data"]["app_name"] == "SkillSathi"


def test_app_version():
    response = client.get("/api/v1/version")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["app_name"] == "SkillSathi"
    assert "Vocational Education" in data["data"]["problem_statement"]


def test_database_health_endpoint():
    response = client.get("/api/v1/health/database")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "status" in data["data"]
