"""
Integration tests for FastAPI endpoints using TestClient.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "Support Intelligence API"
    assert "SpotifyCares" in data["brand"]


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["brand"] == "SpotifyCares"


def test_intents_endpoint():
    response = client.get("/api/intents")
    assert response.status_code == 200
    data = response.json()
    assert "intents" in data
    assert len(data["intents"]) >= 8


def test_metrics_endpoint():
    response = client.get("/api/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "metrics" in data
    assert "Intent Accuracy" in data["metrics"]


def test_failures_endpoint():
    response = client.get("/api/failures")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    assert data[0]["rank"] == 1


def test_decisions_endpoint():
    response = client.get("/api/decisions")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 10
    assert data[0]["decision_id"] == "DEC-01"


def test_analyze_endpoint_e2e():
    payload = {"message": "How do I update my payment method for my subscription?"}
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "intent" in data
    assert "draft_reply" in data
    assert data["decision"] in ["AUTO_HANDLE", "ESCALATE"]
    assert "reason" in data
    assert isinstance(data["evidence"], list)


def test_analyze_endpoint_empty_message():
    response = client.post("/api/analyze", json={"message": "   "})
    assert response.status_code == 400
