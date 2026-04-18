"""Experiment 1: Logistic Regression (Baseline)"""
import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

TRAIN_PATH = "/data/processed/train.csv"
TEST_PATH  = "/data/processed/test.csv"
TARGET     = "Loan_Approval_Status"

df_train = pd.read_csv(TRAIN_PATH)
df_test  = pd.read_csv(TEST_PATH)
X_train, y_train = df_train.drop(columns=[TARGET]), df_train[TARGET]
X_test,  y_test  = df_test.drop(columns=[TARGET]),  df_test[TARGET]

mlflow.set_experiment("FinPredict_LoanApproval")

with mlflow.start_run(run_name="LogisticRegression"):
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    mlflow.log_param("model", "LogisticRegression")
    mlflow.log_param("max_iter", 1000)
    mlflow.log_metrics({
        "accuracy": accuracy_score(y_test, preds),
        "f1_score": f1_score(y_test, preds),
        "roc_auc":  roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
    })
    mlflow.sklearn.log_model(model, "logistic_regression_model")
    print("Logistic Regression experiment logged to MLflow")
