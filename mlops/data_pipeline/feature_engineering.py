"""Task 4: Feature engineering"""
import pandas as pd
import json
import logging

logger = logging.getLogger(__name__)

CLEAN_PATH    = "/data/processed/cleaned.csv"
FEATURE_PATH  = "/data/processed/featured.csv"
BASELINE_PATH = "/data/features/feature_baseline.json"


def engineer_features():
    logger.info("Engineering features...")
    df = pd.read_csv(CLEAN_PATH)
    df["Debt_to_Income_Ratio"]    = df["Outstanding_Debt"] / df["Annual_Income"]
    df["Loan_to_Income_Ratio"]    = df["Loan_Amount_Requested"] / df["Annual_Income"]
    df["Expense_to_Income_Ratio"] = (df["Monthly_Expenses"] * 12) / df["Annual_Income"]
    num_cols = ["Annual_Income", "Credit_Score", "Outstanding_Debt",
                "Loan_Amount_Requested", "Debt_to_Income_Ratio"]
    baseline = {}
    for col in num_cols:
        baseline[col] = {
            "mean": float(df[col].mean()),
            "std":  float(df[col].std()),
            "min":  float(df[col].min()),
            "max":  float(df[col].max()),
        }
    with open(BASELINE_PATH, "w") as f:
        json.dump(baseline, f, indent=2)
    df.to_csv(FEATURE_PATH, index=False)
    logger.info(f"Feature engineering complete. Shape: {df.shape}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    engineer_features()
