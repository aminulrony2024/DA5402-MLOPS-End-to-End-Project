"""Task 7: Train XGBoost model directly inside Airflow task"""
import logging
import pandas as pd
import mlflow
import mlflow.xgboost
from mlflow.tracking import MlflowClient
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

logger = logging.getLogger(__name__)

TRAIN_PATH = "/data/processed/train.csv"
TEST_PATH  = "/data/processed/test.csv"
TARGET     = "Loan_Approval_Status"
MLFLOW_URI = "http://mlflow:5000"
MODEL_NAME = "FinPredict_XGBoost"


def trigger_training():
    logger.info("Loading train/test data...")
    df_train = pd.read_csv(TRAIN_PATH)
    df_test  = pd.read_csv(TEST_PATH)

    X_train = df_train.drop(columns=[TARGET])
    y_train = df_train[TARGET]
    X_test  = df_test.drop(columns=[TARGET])
    y_test  = df_test[TARGET]

    logger.info(f"Train: {X_train.shape} | Test: {X_test.shape}")

    # Train model
    model = XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        scale_pos_weight=(y_train == 0).sum() / (y_train == 1).sum(),
        eval_metric="logloss",
        random_state=42
    )

    logger.info("Training XGBoost model...")
    model.fit(X_train, y_train)

    # Evaluate
    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": round(accuracy_score(y_test, preds), 4),
        "f1_score": round(f1_score(y_test, preds), 4),
        "roc_auc":  round(roc_auc_score(y_test, probs), 4),
    }
    logger.info(f"Metrics: {metrics}")

    # Log to MLflow
    try:
        mlflow.set_tracking_uri(MLFLOW_URI)
        mlflow.set_experiment("FinPredict_LoanApproval")
        with mlflow.start_run(run_name="XGBoost_Airflow"):
            mlflow.log_params({
                "n_estimators": 200,
                "max_depth": 6,
                "learning_rate": 0.1
            })
            mlflow.log_metrics(metrics)
            mlflow.xgboost.log_model(
                model,
                "loan_approval_model",
                registered_model_name=MODEL_NAME
            )

        # ── Auto-promote to Production ─────────────────────────
        client = MlflowClient(MLFLOW_URI)
        latest_version = client.get_latest_versions(MODEL_NAME)[-1].version
        client.transition_model_version_stage(
            name=MODEL_NAME,
            version=latest_version,
            stage="Production",
            archive_existing_versions=True  # archives old Production version
        )
        logger.info(f"Model version {latest_version} promoted to Production automatically")
        # ───────────────────────────────────────────────────────

    except Exception as e:
        logger.warning(f"MLflow logging skipped: {e}")
        logger.info("Training completed successfully without MLflow")

    logger.info("trigger_training task completed successfully")