"""Task 6: Train/test split"""
import pandas as pd
from sklearn.model_selection import train_test_split
import logging

logger = logging.getLogger(__name__)

ENCODED_PATH = "/data/processed/encoded.csv"
TRAIN_PATH   = "/data/processed/train.csv"
TEST_PATH    = "/data/processed/test.csv"
TARGET = "Loan_Approval_Status"

def split_and_save():
    logger.info("Splitting data into train/test sets...")
    df = pd.read_csv(ENCODED_PATH)
    train, test = train_test_split(
        df, test_size=0.2, random_state=42, stratify=df[TARGET]
    )
    train.to_csv(TRAIN_PATH, index=False)
    test.to_csv(TEST_PATH, index=False)
    logger.info(f"Train: {len(train)} rows | Test: {len(test)} rows")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    split_and_save()
