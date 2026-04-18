"""Unit tests for health endpoints"""
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_health_returns_200():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_ready_returns_200():
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"
