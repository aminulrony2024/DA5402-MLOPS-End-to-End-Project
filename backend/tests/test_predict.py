"""Unit tests for prediction endpoint"""
import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

SAMPLE_PAYLOAD = {
    "gender": "Male", "age": 35, "marital_status": "Married",
    "dependents": 1, "education": "Graduate",
    "employment_status": "Employed", "occupation_type": "Salaried",
    "residential_status": "Own", "city_town": "Urban",
    "annual_income": 85000, "monthly_expenses": 2500,
    "credit_score": 720, "existing_loans": 1,
    "total_existing_loan_amount": 15000, "outstanding_debt": 8000,
    "loan_history": 0, "loan_amount_requested": 20000,
    "loan_term": 120, "loan_purpose": "Home",
    "interest_rate": 8.5, "loan_type": "Secured",
    "co_applicant": "Yes", "bank_account_history": 5,
    "transaction_frequency": 15
}


def test_predict_returns_200():
    response = client.post("/api/v1/predict", json=SAMPLE_PAYLOAD)
    assert response.status_code == 200


def test_predict_response_has_required_fields():
    response = client.post("/api/v1/predict", json=SAMPLE_PAYLOAD)
    data = response.json()
    assert "loan_approved" in data
    assert "approval_probability" in data
    assert "risk_level" in data
    assert "message" in data


def test_predict_probability_between_0_and_1():
    response = client.post("/api/v1/predict", json=SAMPLE_PAYLOAD)
    prob = response.json()["approval_probability"]
    assert 0.0 <= prob <= 1.0


def test_predict_invalid_payload_returns_422():
    response = client.post("/api/v1/predict", json={"gender": "Unknown"})
    assert response.status_code == 422
