"""Prediction endpoint"""
import logging
import time
import mlflow
import numpy as np
from fastapi import APIRouter, HTTPException
from api.schemas.request import LoanApplication
from api.schemas.response import PredictionResponse
from model.predictor import get_predictor
from model.preprocessor import preprocess_input
from monitoring.metrics import PREDICTION_LATENCY, PREDICTION_COUNTER, DATA_DRIFT_SCORE

logger = logging.getLogger(__name__)
router = APIRouter()

# Baseline statistics from training data
BASELINE = {
    "Annual_Income":   {"mean": 83588.47, "std": 35720.85},
    "Credit_Score":    {"mean": 678.09,   "std": 159.99},
    "Outstanding_Debt":{"mean": 14984.86, "std": 8663.40},
}


def calculate_drift_score(application: LoanApplication) -> float:
    """
    Simple Z-score based drift detection.
    Returns score 0-1 where >0.1 means drift detected.
    """
    z_scores = []
    values = {
        "Annual_Income":    application.annual_income,
        "Credit_Score":     application.credit_score,
        "Outstanding_Debt": application.outstanding_debt,
    }
    for feature, value in values.items():
        mean = BASELINE[feature]["mean"]
        std  = BASELINE[feature]["std"]
        if std > 0:
            z = abs((value - mean) / std)
            z_scores.append(min(z / 10, 1.0))  # normalize to 0-1

    return round(float(np.mean(z_scores)), 4) if z_scores else 0.0


@router.post("/predict", response_model=PredictionResponse)
def predict(application: LoanApplication):
    """
    Predict loan approval status.
    - **Input**: Applicant financial and personal details
    - **Output**: Approval status, probability, risk level
    """
    start_time = time.time()
    try:
        # Calculate and expose drift score
        drift_score = calculate_drift_score(application)
        DATA_DRIFT_SCORE.set(drift_score)

        if drift_score > 0.1:
            logger.warning(f"Data drift detected! Score: {drift_score}")

        predictor = get_predictor()
        result = predictor.predict(application)

        latency = time.time() - start_time
        PREDICTION_LATENCY.observe(latency)
        PREDICTION_COUNTER.labels(status="success").inc()

        logger.info(
            f"Prediction done in {latency:.4f}s | "
            f"Approved: {result.loan_approved} | "
            f"Drift: {drift_score}"
        )
        return result

    except Exception as e:
        PREDICTION_COUNTER.labels(status="error").inc()
        logger.error(f"Prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/feedback")
def submit_feedback(
    applicant_id: str,
    predicted: int,
    actual_outcome: int
):
    """
    Log ground truth label for a previous prediction.
    Used to calculate real-world model performance decay.
    """
    logger.info(
        f"Feedback received | ID: {applicant_id} | "
        f"Predicted: {predicted} | Actual: {actual_outcome} | "
        f"Correct: {predicted == actual_outcome}"
    )
    # Log to MLflow
    with mlflow.start_run(run_name="feedback"):
        mlflow.log_metric("prediction_correct",
                          int(predicted == actual_outcome))
    return {"status": "feedback logged", "correct": predicted == actual_outcome}
