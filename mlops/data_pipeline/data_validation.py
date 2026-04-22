"""Task 2: Validate schema and data quality"""
import pandas as pd
import logging

logger = logging.getLogger(__name__)

STAGE_PATH = "/data/processed/staged.csv"

REQUIRED_COLUMNS = [
    'Applicant_ID', 'Gender', 'Age', 'Marital_Status', 'Dependents',
    'Education', 'Employment_Status', 'Occupation_Type', 'Residential_Status',
    'City/Town', 'Annual_Income', 'Monthly_Expenses', 'Credit_Score',
    'Existing_Loans', 'Total_Existing_Loan_Amount', 'Outstanding_Debt',
    'Loan_History', 'Loan_Amount_Requested', 'Loan_Term', 'Loan_Purpose',
    'Interest_Rate', 'Loan_Type', 'Co-Applicant', 'Bank_Account_History',
    'Transaction_Frequency', 'Default_Risk', 'Loan_Approval_Status'
]


def validate_schema():
    logger.info("Validating schema and data quality...")
    df = pd.read_csv(STAGE_PATH)
    missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing columns: {missing_cols}")
    null_counts = df.isnull().sum()
    if null_counts.any():
        logger.warning(f"Null values found:\n{null_counts[null_counts > 0]}")
    assert len(df) > 0, "Dataset is empty after ingestion"
    assert df['Credit_Score'].between(300, 900).all(), "Invalid Credit_Score values"
    assert set(df['Loan_Approval_Status'].unique()).issubset({0, 1}), "Invalid target values"
    logger.info(f"Validation passed. Rows: {len(df)}, Columns: {len(df.columns)}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    validate_schema()
