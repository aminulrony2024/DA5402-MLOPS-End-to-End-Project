"""Experiment 3: XGBoost (Production Model)"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mlflow
import mlflow.xgboost
from xgboost import XGBClassifier
from sklearn.metrics import (
    accuracy_score, f1_score, roc_auc_score,
    precision_score, recall_score,
    confusion_matrix, classification_report
)

TRAIN_PATH = "data/processed/train.csv"
TEST_PATH  = "data/processed/test.csv"
TARGET     = "Loan_Approval_Status"

df_train = pd.read_csv(TRAIN_PATH)
df_test  = pd.read_csv(TEST_PATH)
X_train, y_train = df_train.drop(columns=[TARGET]), df_train[TARGET]
X_test,  y_test  = df_test.drop(columns=[TARGET]),  df_test[TARGET]

mlflow.set_tracking_uri("http://localhost:5000") 
mlflow.set_experiment("FinPredict_LoanApproval")

# ── Enable Autolog ──────────────────────────────────────────────
mlflow.xgboost.autolog()

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
    probs = model.predict_proba(X_test)[:, 1]

    # ── Standard params (autolog handles most, we add extras) ───
    mlflow.log_params({
        "model":               "XGBoost",
        "n_estimators":        200,
        "max_depth":           6,
        "learning_rate":       0.1,
        "scale_pos_weight":    1.8,
        "dataset_version":     "v2-processed",
        "train_size":          len(X_train),
        "test_size":           len(X_test),
        "num_features":        X_train.shape[1],
        "class_imbalance_ratio": round(
            (y_train == 0).sum() / (y_train == 1).sum(), 3
        ),
    })

    # ── Standard ML metrics ─────────────────────────────────────
    mlflow.log_metrics({
        "accuracy":  round(accuracy_score(y_test, preds), 4),
        "f1_score":  round(f1_score(y_test, preds), 4),
        "roc_auc":   round(roc_auc_score(y_test, probs), 4),
        "precision": round(precision_score(y_test, preds), 4),
        "recall":    round(recall_score(y_test, preds), 4),
    })

    # ── Confusion matrix metrics (beyond autolog) ────────────────
    cm = confusion_matrix(y_test, preds)
    mlflow.log_metrics({
        "true_negatives":  int(cm[0][0]),
        "false_positives": int(cm[0][1]),
        "false_negatives": int(cm[1][0]),
        "true_positives":  int(cm[1][1]),
    })

    # ── Business metrics (beyond autolog) ───────────────────────
    false_negative_rate = round(cm[1][0] / (cm[1][0] + cm[1][1]), 4)
    false_positive_rate = round(cm[0][1] / (cm[0][0] + cm[0][1]), 4)
    mlflow.log_metrics({
        "false_negative_rate": false_negative_rate,  # wrongly rejected loans
        "false_positive_rate": false_positive_rate,  # wrongly approved loans
    })

    # ── Feature importance artifact (beyond autolog) ─────────────
    feat_imp = pd.Series(
        model.feature_importances_,
        index=X_train.columns
    ).sort_values(ascending=False).head(15)

    fig, ax = plt.subplots(figsize=(10, 6))
    feat_imp.plot(kind='bar', ax=ax, color='steelblue')
    ax.set_title("Top 15 Feature Importances — XGBoost")
    ax.set_xlabel("Feature")
    ax.set_ylabel("Importance Score")
    plt.tight_layout()
    plt.savefig("feature_importance.png")
    mlflow.log_artifact("feature_importance.png")
    plt.close()
    os.remove("feature_importance.png")

    # ── Classification report as artifact (beyond autolog) ───────
    report = classification_report(y_test, preds,
                                   target_names=["Rejected", "Approved"])
    with open("classification_report.txt", "w") as f:
        f.write(report)
    mlflow.log_artifact("classification_report.txt")
    os.remove("classification_report.txt")

    # ── Feature baseline stats as artifact (beyond autolog) ──────
    baseline = {}
    for col in ["Annual_Income", "Credit_Score", "Outstanding_Debt",
                "Loan_Amount_Requested", "Debt_to_Income_Ratio"]:
        if col in X_train.columns:
            baseline[col] = {
                "mean": round(float(X_train[col].mean()), 4),
                "std":  round(float(X_train[col].std()), 4),
                "min":  round(float(X_train[col].min()), 4),
                "max":  round(float(X_train[col].max()), 4),
            }

    import json
    with open("feature_baseline.json", "w") as f:
        json.dump(baseline, f, indent=2)
    mlflow.log_artifact("feature_baseline.json")
    os.remove("feature_baseline.json")

    # ── Log model ────────────────────────────────────────────────
    mlflow.xgboost.log_model(
        model, "xgboost_model"
    )

    print("XGBoost experiment logged to MLflow")
    print(f"Accuracy:  {accuracy_score(y_test, preds):.4f}")
    print(f"F1 Score:  {f1_score(y_test, preds):.4f}")
    print(f"ROC-AUC:   {roc_auc_score(y_test, probs):.4f}")
    print(f"Precision: {precision_score(y_test, preds):.4f}")
    print(f"Recall:    {recall_score(y_test, preds):.4f}")
    print("\nClassification Report:")
    print(report)