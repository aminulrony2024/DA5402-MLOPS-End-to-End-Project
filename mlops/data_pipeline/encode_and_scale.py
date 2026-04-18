"""Task 5: Encode categoricals and scale numerics"""
import pandas as pd
import pickle
import logging
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)

FEATURE_PATH = "/data/processed/featured.csv"
ENCODED_PATH = "/data/processed/encoded.csv"
SCALER_PATH = "/data/features/scaler.pkl"


def encode_and_scale():
    logger.info("Encoding and scaling features...")
    df = pd.read_csv(FEATURE_PATH)

    # Binary label encoding
    df["Gender"] = df["Gender"].map({"Male": 1, "Female": 0})
    df["Loan_Type"] = df["Loan_Type"].map({"Secured": 1, "Unsecured": 0})
    df["Co_Applicant"] = df["Co_Applicant"].map({"Yes": 1, "No": 0})

    # Ordinal encoding
    df["Education"] = df["Education"].map({"High School": 0, "Graduate": 1, "Postgraduate": 2})

    # One-hot encoding
    ohe_cols = [
        "Marital_Status", "Employment_Status", "Occupation_Type",
        "Residential_Status", "City_Town", "Loan_Purpose"
    ]
    df = pd.get_dummies(df, columns=ohe_cols, drop_first=False)

    # Standard scaling on numeric columns
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

    df.to_csv(ENCODED_PATH, index=False)
    logger.info(f"Encoding complete. Final shape: {df.shape}")
    logger.info(f"Scaler saved to {SCALER_PATH}")
