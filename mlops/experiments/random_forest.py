"""Experiment 2: Random Forest"""
import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

TRAIN_PATH = "/data/processed/train.csv"
TEST_PATH  = "/data/processed/test.csv"
TARGET     = "Loan_Approval_Status"

df_train = pd.read_csv(TRAIN_PATH)
df_test  = pd.read_csv(TEST_PATH)
X_train, y_train = df_train.drop(columns=[TARGET]), df_train[TARGET]
X_test,  y_test  = df_test.drop(columns=[TARGET]),  df_test[TARGET]

mlflow.set_experiment("FinPredict_LoanApproval")

with mlflow.start_run(run_name="RandomForest"):
    model = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    mlflow.log_params({"n_estimators": 100, "max_depth": 8, "model": "RandomForest"})
    mlflow.log_metrics({
        "accuracy": accuracy_score(y_test, preds),
        "f1_score": f1_score(y_test, preds),
        "roc_auc":  roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
    })
    mlflow.sklearn.log_model(model, "random_forest_model")
    print("Random Forest experiment logged to MLflow")
