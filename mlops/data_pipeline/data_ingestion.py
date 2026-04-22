"""Task 1: Load raw CSV data"""
import pandas as pd
import logging

logger = logging.getLogger(__name__)

RAW_PATH = "/data/raw/Loan_Dataset.csv"
STAGE_PATH = "/data/processed/staged.csv"


def load_raw_data():
    logger.info("Starting data ingestion...")
    df = pd.read_csv(RAW_PATH)
    logger.info(f"Loaded {len(df)} rows, {len(df.columns)} columns")
    assert len(df) > 0, "Dataset is empty"
    df.to_csv(STAGE_PATH, index=False)
    logger.info(f"Staged data saved to {STAGE_PATH}")
    return STAGE_PATH