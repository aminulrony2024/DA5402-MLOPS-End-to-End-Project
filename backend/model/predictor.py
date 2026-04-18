"""Prediction logic"""
import logging
from model.loader import load_model
from model.preprocessor import preprocess_input
from api.schemas.request import LoanApplication
from api.schemas.response import PredictionResponse

logger = logging.getLogger(__name__)


class LoanPredictor:
    def __init__(self):
        self.model = load_model()
        logger.info("LoanPredictor initialized")

    def predict(self, application: LoanApplication) -> PredictionResponse:
        input_df = preprocess_input(application)
        probability = float(self.model.predict_proba(input_df)[0][1])
        approved = probability >= 0.5

        risk_level = (
            "Low" if probability > 0.75 else
            "Medium" if probability > 0.5 else
            "High"
        )
        credit_impact = (
            "Strong positive factor" if application.credit_score >= 750 else
            "Positive factor" if application.credit_score >= 650 else
            "Needs improvement"
        )
        recommendation = (
            "Your application meets our approval criteria." if approved else
            "Consider improving your credit score or reducing outstanding debt."
        )

        return PredictionResponse(
            loan_approved=approved,
            approval_probability=round(probability, 4),
            risk_level=risk_level,
            message="Loan Approved" if approved else "Loan Rejected",
            credit_score_impact=credit_impact,
            recommendation=recommendation
        )


_predictor_instance = None


def get_predictor() -> LoanPredictor:
    global _predictor_instance
    if _predictor_instance is None:
        _predictor_instance = LoanPredictor()
    return _predictor_instance
