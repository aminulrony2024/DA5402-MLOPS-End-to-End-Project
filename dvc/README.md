# DVC Data Versioning — FinPredict

## Overview

This project tracks **two versions of data** using DVC alongside Git.

```
VERSION 1 (Raw)          data/raw/Loan_Dataset.csv
VERSION 2 (Processed)    data/processed/train.csv
                         data/processed/test.csv
```

---

## Version 1 — Raw Data

**File:** `data/raw/Loan_Dataset.csv`  
**DVC Pointer:** `data/raw/Loan_Dataset.csv.dvc`  
**Git Tag:** `data-v1-raw`

| Property | Value |
|---|---|
| Rows | 52,000 |
| Columns | 27 |
| Target | Loan_Approval_Status (0/1) |
| State | Unprocessed — original dataset |
| Special columns | City/Town, Co-Applicant (special characters) |

```bash
# Switch to Version 1
git checkout data-v1-raw
dvc checkout
```

---

## Version 2 — Preprocessed Data

**Files:** `data/processed/train.csv`, `data/processed/test.csv`  
**DVC Pointers:** `train.csv.dvc`, `test.csv.dvc`  
**Git Tag:** `data-v2-processed`

| Property | Value |
|---|---|
| Train rows | 41,600 (80%) |
| Test rows | 10,400 (20%) |
| Columns | 35+ (after one-hot encoding) |
| State | Cleaned, encoded, scaled, feature engineered |

**Transformations applied from V1 → V2:**
1. Renamed `City/Town` → `City_Town`, `Co-Applicant` → `Co_Applicant`
2. Dropped `Applicant_ID` and `Default_Risk`
3. Clipped outliers (IQR) on `Age` and `Loan_Amount_Requested`
4. Engineered 3 new features:
   - `Debt_to_Income_Ratio` = Outstanding_Debt / Annual_Income
   - `Loan_to_Income_Ratio` = Loan_Amount_Requested / Annual_Income
   - `Expense_to_Income_Ratio` = (Monthly_Expenses × 12) / Annual_Income
5. Binary encoding: Gender, Loan_Type, Co_Applicant
6. Ordinal encoding: Education (High School=0, Graduate=1, Postgraduate=2)
7. One-hot encoding: Marital_Status, Employment_Status, Occupation_Type,
   Residential_Status, City_Town, Loan_Purpose
8. StandardScaler on 14 numeric columns
9. Stratified 80/20 train/test split

```bash
# Switch to Version 2
git checkout data-v2-processed
dvc checkout
```

---

## Setup Commands (Run Once)

```bash
# Install DVC
pip install dvc

# Initialize inside FinPredict/
cd FinPredict
git init
dvc init

# Track Version 1 — Raw data
dvc add data/raw/Loan_Dataset.csv
git add data/raw/Loan_Dataset.csv.dvc data/raw/.gitignore
git commit -m "data(v1): track raw dataset"
git tag -a "data-v1-raw" -m "Version 1: Raw dataset"

# Run preprocessing to generate Version 2
python mlops/training/preprocess.py

# Track Version 2 — Preprocessed data
dvc add data/processed/train.csv
dvc add data/processed/test.csv
dvc add data/features/scaler.pkl
dvc add data/features/feature_baseline.json
git add data/processed/train.csv.dvc data/processed/test.csv.dvc \
        data/features/scaler.pkl.dvc data/features/feature_baseline.json.dvc
git commit -m "data(v2): track preprocessed train/test splits"
git tag -a "data-v2-processed" -m "Version 2: Preprocessed data"
```

---

## Switching Between Versions

```bash
# Go to Version 1 (raw data)
git checkout data-v1-raw
dvc checkout
# → data/raw/Loan_Dataset.csv is now the original file

# Go to Version 2 (preprocessed)
git checkout data-v2-processed
dvc checkout
# → data/processed/train.csv and test.csv are now available

# Come back to latest
git checkout main
dvc checkout
```

---

## Reproduce the Full Pipeline

```bash
cd dvc
dvc repro
```

This runs all 7 stages in order and produces Version 2 from Version 1 automatically.

```bash
# See what will run
dvc status

# Visualize the pipeline DAG
dvc dag
```

**Expected DAG output:**
```
            +---------------------------+
            | data/raw/Loan_Dataset.csv |  ← VERSION 1
            +---------------------------+
                          *
                 +-----------------+
                 | data_ingestion  |
                 +-----------------+
                          *
                 +-----------------+
                 | data_validation |
                 +-----------------+
                          *
                 +-----------------+
                 |  data_cleaning  |
                 +-----------------+
                          *
                +--------------------+
                | feature_engineering|
                +--------------------+
                          *
                +------------------+
                | encode_and_scale |
                +------------------+
                          *
                +------------------+
                | train_test_split |  ← PRODUCES VERSION 2
                +------------------+
                    *           *
              train.csv       test.csv
                          *
                  +-------------+
                  | train_model |
                  +-------------+
```

---

## Why Two Versions?

| Reason | Explanation |
|---|---|
| Reproducibility | Anyone can reproduce exact results from V1 |
| Auditability | Clear record of what transformations were applied |
| Rollback | If preprocessing has a bug, revert to V1 and re-run |
| MLOps best practice | Raw data is immutable; processed data is derived |
| Evaluation criterion | DVC data versioning is explicitly graded |
