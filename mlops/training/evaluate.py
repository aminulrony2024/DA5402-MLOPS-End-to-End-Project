"""
Model evaluation — generates a classification report and saves metrics to JSON
"""
import json
import logging
import pandas as pd
import mlflow
from sklearn.metrics import (
    accuracy_score, f1_score, roc_auc_score,
    precision_score, recall_score, confusion_matrix,
    classification_report
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TEST_PATH    = "/data/processed/test.csv"
METRICS_PATH = "metrics.json"
TARGET       = "Loan_Approval_Status"
MLFLOW_URI   = "http://localhost:5000"
MODEL_NAME   = "FinPredict_XGBoost"


def evaluate():
    mlflow.set_tracking_uri(MLFLOW_URI)

    # Load production model
    model = mlflow.xgboost.load_model(f"models:/{MODEL_NAME}/Production")

    df = pd.read_csv(TEST_PATH)
    X_test = df.drop(columns=[TARGET])
    y_test = df[TARGET]

    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy":  round(accuracy_score(y_test, preds), 4),
        "f1_score":  round(f1_score(y_test, preds), 4),
        "roc_auc":   round(roc_auc_score(y_test, probs), 4),
        "precision": round(precision_score(y_test, preds), 4),
        "recall":    round(recall_score(y_test, preds), 4),
    }

    cm = confusion_matrix(y_test, preds)
    metrics["true_negatives"]  = int(cm[0][0])
    metrics["false_positives"] = int(cm[0][1])
    metrics["false_negatives"] = int(cm[1][0])
    metrics["true_positives"]  = int(cm[1][1])

    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=2)

    logger.info("=== Evaluation Report ===")
    for k, v in metrics.items():
        logger.info(f"  {k}: {v}")
    logger.info("\n" + classification_report(y_test, preds))
    logger.info(f"Metrics saved to {METRICS_PATH}")

    return metrics


if __name__ == "__main__":
    evaluate()
