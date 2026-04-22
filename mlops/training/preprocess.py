"""
Standalone preprocessing script for training pipeline.
Runs the full preprocessing sequence end-to-end without Airflow.
Use this for quick re-runs during development.
"""
import logging
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RAW_PATH    = "data/raw/Loan_Dataset.csv"
TRAIN_PATH  = "data/processed/train.csv"
TEST_PATH   = "data/processed/test.csv"
SCALER_PATH = "data/features/scaler.pkl"
TARGET      = "Loan_Approval_Status"


def run_preprocessing():
    logger.info("Loading raw data...")
    df = pd.read_csv(RAW_PATH)
    logger.info(f"Loaded: {df.shape}")

    # Rename columns
    df = df.rename(columns={"City/Town": "City_Town", "Co-Applicant": "Co_Applicant"})

    # Drop unused columns
    df = df.drop(columns=["Applicant_ID", "Default_Risk"], errors="ignore")

    # Clip outliers
    for col in ["Age", "Loan_Amount_Requested"]:
        Q1, Q3 = df[col].quantile(0.25), df[col].quantile(0.75)
        IQR = Q3 - Q1
        df[col] = df[col].clip(Q1 - 1.5 * IQR, Q3 + 1.5 * IQR)

    # Feature engineering
    df["Debt_to_Income_Ratio"]    = df["Outstanding_Debt"] / df["Annual_Income"]
    df["Loan_to_Income_Ratio"]    = df["Loan_Amount_Requested"] / df["Annual_Income"]
    df["Expense_to_Income_Ratio"] = (df["Monthly_Expenses"] * 12) / df["Annual_Income"]

    # Binary encoding
    df["Gender"]       = df["Gender"].map({"Male": 1, "Female": 0})
    df["Loan_Type"]    = df["Loan_Type"].map({"Secured": 1, "Unsecured": 0})
    df["Co_Applicant"] = df["Co_Applicant"].map({"Yes": 1, "No": 0})
    df["Education"]    = df["Education"].map({"High School": 0, "Graduate": 1, "Postgraduate": 2})

    # One-hot encoding
    ohe_cols = [
        "Marital_Status", "Employment_Status", "Occupation_Type",
        "Residential_Status", "City_Town", "Loan_Purpose"
    ]
    df = pd.get_dummies(df, columns=ohe_cols, drop_first=False)

    # Scale numeric columns
    num_cols = [
        "Age", "Annual_Income", "Monthly_Expenses", "Credit_Score",
        "Total_Existing_Loan_Amount", "Outstanding_Debt",
        "Loan_Amount_Requested", "Loan_Term", "Interest_Rate",
        "Bank_Account_History", "Transaction_Frequency",
        "Debt_to_Income_Ratio", "Loan_to_Income_Ratio", "Expense_to_Income_Ratio"
    ]
    scaler = StandardScaler()
    df[num_cols] = scaler.fit_transform(df[num_cols])

    with open(SCALER_PATH, "wb") as f:
        pickle.dump(scaler, f)

    # Train/test split
    train, test = train_test_split(
        df, test_size=0.2, random_state=42, stratify=df[TARGET]
    )
    train.to_csv(TRAIN_PATH, index=False)
    test.to_csv(TEST_PATH, index=False)

    logger.info(f"Train: {len(train)} | Test: {len(test)}")
    logger.info("Preprocessing complete.")


if __name__ == "__main__":
    run_preprocessing()
