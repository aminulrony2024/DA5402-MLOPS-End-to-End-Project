"""Output schema for prediction response"""
from pydantic import BaseModel


class PredictionResponse(BaseModel):
    loan_approved: bool
    approval_probability: float
    risk_level: str
    message: str
    credit_score_impact: str
    recommendation: str
