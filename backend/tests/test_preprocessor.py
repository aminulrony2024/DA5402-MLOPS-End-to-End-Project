"""Unit tests for preprocessor"""
import pandas as pd
from api.schemas.request import LoanApplication
from model.preprocessor import preprocess_input

SAMPLE_APP = LoanApplication(
    gender="Male", age=35, marital_status="Married",
    dependents=1, education="Graduate",
    employment_status="Employed", occupation_type="Salaried",
    residential_status="Own", city_town="Urban",
    annual_income=85000, monthly_expenses=2500,
    credit_score=720, existing_loans=1,
    total_existing_loan_amount=15000, outstanding_debt=8000,
    loan_history=0, loan_amount_requested=20000,
    loan_term=120, loan_purpose="Home",
    interest_rate=8.5, loan_type="Secured",
    co_applicant="Yes", bank_account_history=5,
    transaction_frequency=15
)


def test_preprocess_returns_dataframe():
    result = preprocess_input(SAMPLE_APP)
    assert isinstance(result, pd.DataFrame)


def test_preprocess_has_one_row():
    result = preprocess_input(SAMPLE_APP)
    assert result.shape[0] == 1


def test_debt_to_income_ratio():
    result = preprocess_input(SAMPLE_APP)
    expected = 8000 / 85000
    assert abs(result["Debt_to_Income_Ratio"].iloc[0] - expected) < 1e-6


def test_gender_encoded_correctly():
    result = preprocess_input(SAMPLE_APP)
    assert result["Gender"].iloc[0] == 1  # Male = 1
