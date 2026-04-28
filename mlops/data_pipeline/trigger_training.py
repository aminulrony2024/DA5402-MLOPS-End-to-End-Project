"""Task 7: Train XGBoost model directly inside Airflow task"""
import os
import json
import logging
import pandas as pd
import matplotlib.pyplot as plt
import mlflow
import mlflow.xgboost
from mlflow.tracking import MlflowClient
from xgboost import XGBClassifier
from sklearn.metrics import (
    accuracy_score, f1_score, roc_auc_score,
    precision_score, recall_score,
    confusion_matrix, classification_report
)

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

    # ── Compute class imbalance ratio ───────────────────────────
    class_imbalance_ratio = round(
        (y_train == 0).sum() / (y_train == 1).sum(), 3
    )

    # ── Train model ─────────────────────────────────────────────
    model = XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        scale_pos_weight=class_imbalance_ratio,
        eval_metric="logloss",
        random_state=42
    )
    logger.info("Training XGBoost model...")
    model.fit(X_train, y_train)

    # ── Evaluate ─────────────────────────────────────────────────
    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:, 1]
    cm    = confusion_matrix(y_test, preds)
    tn, fp, fn, tp = cm[0][0], cm[0][1], cm[1][0], cm[1][1]

    # Standard ML metrics
    metrics = {
        "accuracy":  round(accuracy_score(y_test, preds), 4),
        "f1_score":  round(f1_score(y_test, preds), 4),
        "roc_auc":   round(roc_auc_score(y_test, probs), 4),
        "precision": round(precision_score(y_test, preds), 4),
        "recall":    round(recall_score(y_test, preds), 4),
        # Confusion matrix breakdown
        "true_negatives":  int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "true_positives":  int(tp),
        # Business metrics
        "false_negative_rate": round(fn / (fn + tp), 4),  # wrongly rejected loans
        "false_positive_rate": round(fp / (fp + tn), 4),  # wrongly approved loans
    }
    logger.info(f"Metrics: {metrics}")

    # ── Log to MLflow ────────────────────────────────────────────
    try:
        mlflow.set_tracking_uri(MLFLOW_URI)
        mlflow.set_experiment("FinPredict_LoanApproval")

        # Disable autolog — prevents it overwriting manual logs
        mlflow.xgboost.autolog(disable=True)

        with mlflow.start_run(run_name="XGBoost_Airflow"):

            # ── All params ───────────────────────────────────────
            mlflow.log_params({
                "model":                 "XGBoost",
                "n_estimators":          200,
                "max_depth":             6,
                "learning_rate":         0.1,
                "scale_pos_weight":      class_imbalance_ratio,
                "dataset_version":       "v2-processed",
                "train_size":            len(X_train),
                "test_size":             len(X_test),
                "num_features":          X_train.shape[1],
                "class_imbalance_ratio": class_imbalance_ratio,
            })

            # ── All metrics ──────────────────────────────────────
            mlflow.log_metrics(metrics)

            # ── Feature importance artifact ──────────────────────
            feat_imp = pd.Series(
                model.feature_importances_,
                index=X_train.columns
            ).sort_values(ascending=False).head(15)

            fig, ax = plt.subplots(figsize=(10, 6))
            feat_imp.plot(kind="bar", ax=ax, color="steelblue")
            ax.set_title("Top 15 Feature Importances — XGBoost")
            ax.set_xlabel("Feature")
            ax.set_ylabel("Importance Score")
            plt.tight_layout()
            plt.savefig("/tmp/feature_importance.png")
            mlflow.log_artifact("/tmp/feature_importance.png")
            plt.close()
            os.remove("/tmp/feature_importance.png")

            # ── Classification report artifact ───────────────────
            report = classification_report(
                y_test, preds,
                target_names=["Rejected", "Approved"]
            )
            with open("/tmp/classification_report.txt", "w") as f:
                f.write(report)
            mlflow.log_artifact("/tmp/classification_report.txt")
            os.remove("/tmp/classification_report.txt")

            # ── Feature baseline stats artifact ──────────────────
            baseline = {}
            for col in ["Annual_Income", "Credit_Score", "Outstanding_Debt",
                        "Loan_Amount_Requested", "Debt_to_Income_Ratio"]:
                if col in X_train.columns:
                    baseline[col] = {
                        "mean": round(float(X_train[col].mean()), 4),
                        "std":  round(float(X_train[col].std()),  4),
                        "min":  round(float(X_train[col].min()),  4),
                        "max":  round(float(X_train[col].max()),  4),
                    }
            with open("/tmp/feature_baseline.json", "w") as f:
                json.dump(baseline, f, indent=2)
            mlflow.log_artifact("/tmp/feature_baseline.json")
            os.remove("/tmp/feature_baseline.json")

            # ── Log model ────────────────────────────────────────
            mlflow.xgboost.log_model(
                model,
                "loan_approval_model",
                registered_model_name=MODEL_NAME
            )

        # ── Auto-promote to Production ───────────────────────────
        client = MlflowClient(MLFLOW_URI)
        latest_version = client.get_latest_versions(MODEL_NAME)[-1].version
        client.transition_model_version_stage(
            name=MODEL_NAME,
            version=latest_version,
            stage="Production",
            archive_existing_versions=True
        )
        logger.info(f"Model v{latest_version} promoted to Production")

    except Exception as e:
        logger.warning(f"MLflow logging skipped: {e}")
        logger.info("Training completed successfully without MLflow")

    logger.info("trigger_training task completed successfully")