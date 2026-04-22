"""Experiment 3: XGBoost (Production Model)"""
import pandas as pd
import mlflow
import mlflow.xgboost
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

TRAIN_PATH = "data/processed/train.csv"
TEST_PATH  = "data/processed/test.csv"
TARGET     = "Loan_Approval_Status"

df_train = pd.read_csv(TRAIN_PATH)
df_test  = pd.read_csv(TEST_PATH)
X_train, y_train = df_train.drop(columns=[TARGET]), df_train[TARGET]
X_test,  y_test  = df_test.drop(columns=[TARGET]),  df_test[TARGET]

mlflow.set_experiment("FinPredict_LoanApproval")

with mlflow.start_run(run_name="XGBoost_Production"):
    model = XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        scale_pos_weight=1.8,
        eval_metric="logloss",
        random_state=42
    )
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    mlflow.log_params({
        "n_estimators": 200,
        "max_depth": 6,
        "learning_rate": 0.1,
        "model": "XGBoost"          # ✅ keep this — register_model.py filters on it
    })
    mlflow.log_metrics({
        "accuracy": accuracy_score(y_test, preds),
        "f1_score": f1_score(y_test, preds),
        "roc_auc":  roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
    })
    mlflow.xgboost.log_model(
        model, "xgboost_model"      # removed registered_model_name — register_model.py handles this
    )
    print("XGBoost experiment logged to MLflow")