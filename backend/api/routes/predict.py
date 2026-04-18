"""Prediction endpoint"""
import logging
import time
from fastapi import APIRouter, HTTPException
from api.schemas.request import LoanApplication
from api.schemas.response import PredictionResponse
from model.predictor import get_predictor
from monitoring.metrics import PREDICTION_LATENCY, PREDICTION_COUNTER

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/predict", response_model=PredictionResponse)
def predict(application: LoanApplication):
    """
    Predict loan approval status.
    - **Input**: Applicant financial and personal details
    - **Output**: Approval status, probability, risk level
    """
    start_time = time.time()
    try:
        predictor = get_predictor()
        result = predictor.predict(application)
        latency = time.time() - start_time
        PREDICTION_LATENCY.observe(latency)
        PREDICTION_COUNTER.labels(status="success").inc()
        logger.info(f"Prediction done in {latency:.4f}s | Approved: {result.loan_approved}")
        return result
    except Exception as e:
        PREDICTION_COUNTER.labels(status="error").inc()
        logger.error(f"Prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
