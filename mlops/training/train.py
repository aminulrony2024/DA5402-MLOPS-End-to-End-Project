"""Main model training script with MLflow tracking"""
import argparse
import logging
import pandas as pd
import mlflow
import mlflow.xgboost
from xgboost import XGBClassifier
from sklearn.metrics import (
    accuracy_score, f1_score, roc_auc_score,
    precision_score, recall_score, classification_report
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

TRAIN_PATH = "/data/processed/train.csv"
TEST_PATH = "/data/processed/test.csv"
TARGET = "Loan_Approval_Status"
MLFLOW_URI = "http://localhost:5000"


def train(n_estimators=200, max_depth=6, learning_rate=0.1):
    df_train = pd.read_csv(TRAIN_PATH)
    df_test = pd.read_csv(TEST_PATH)

    X_train = df_train.drop(columns=[TARGET])
    y_train = df_train[TARGET]
    X_test = df_test.drop(columns=[TARGET])
    y_test = df_test[TARGET]

    mlflow.set_tracking_uri(MLFLOW_URI)
    mlflow.set_experiment("FinPredict_LoanApproval")

    with mlflow.start_run(run_name="XGBoost"):
        model = XGBClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            learning_rate=learning_rate,
            scale_pos_weight=(y_train == 0).sum() / (y_train == 1).sum(),
            eval_metric="logloss",
            random_state=42
        )
        model.fit(X_train, y_train)

        preds = model.predict(X_test)
        probs = model.predict_proba(X_test)[:, 1]

        metrics = {
            "accuracy":  accuracy_score(y_test, preds),
            "f1_score":  f1_score(y_test, preds),
            "roc_auc":   roc_auc_score(y_test, probs),
            "precision": precision_score(y_test, preds),
            "recall":    recall_score(y_test, preds),
        }

        mlflow.log_params({
            "n_estimators": n_estimators,
            "max_depth": max_depth,
            "learning_rate": learning_rate,
        })
        mlflow.log_metrics(metrics)
        mlflow.xgboost.log_model(
            model, "loan_approval_model",
            registered_model_name="FinPredict_XGBoost"
        )

        logger.info(f"Accuracy:  {metrics['accuracy']:.4f}")
        logger.info(f"F1 Score:  {metrics['f1_score']:.4f}")
        logger.info(f"ROC-AUC:   {metrics['roc_auc']:.4f}")
        logger.info(f"Precision: {metrics['precision']:.4f}")
        logger.info(f"Recall:    {metrics['recall']:.4f}")
        logger.info("\n" + classification_report(y_test, preds))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_estimators", type=int, default=200)
    parser.add_argument("--max_depth", type=int, default=6)
    parser.add_argument("--learning_rate", type=float, default=0.1)
    args = parser.parse_args()
    train(args.n_estimators, args.max_depth, args.learning_rate)
