"""Task 3: Clean and rename columns"""
import pandas as pd
import logging

logger = logging.getLogger(__name__)

STAGE_PATH = "/data/processed/staged.csv"
CLEAN_PATH = "/data/processed/cleaned.csv"


def clean_data():
    logger.info("Cleaning data...")
    df = pd.read_csv(STAGE_PATH)
    df = df.rename(columns={"City/Town": "City_Town", "Co-Applicant": "Co_Applicant"})
    df = df.drop(columns=["Applicant_ID", "Default_Risk"], errors='ignore')
    for col in ["Age", "Loan_Amount_Requested"]:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        df[col] = df[col].clip(Q1 - 1.5 * IQR, Q3 + 1.5 * IQR)
    df.to_csv(CLEAN_PATH, index=False)
    logger.info(f"Cleaned data saved: {CLEAN_PATH} | Shape: {df.shape}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    clean_data()
