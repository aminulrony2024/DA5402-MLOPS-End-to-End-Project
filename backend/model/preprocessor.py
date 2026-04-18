"""Preprocess incoming API request to match training pipeline"""
import pandas as pd
from api.schemas.request import LoanApplication

GENDER_MAP = {"Male": 1, "Female": 0}
LOAN_TYPE_MAP = {"Secured": 1, "Unsecured": 0}
CO_APPLICANT_MAP = {"Yes": 1, "No": 0}
EDUCATION_MAP = {"High School": 0, "Graduate": 1, "Postgraduate": 2}


def preprocess_input(app: LoanApplication) -> pd.DataFrame:
    row = {
        "Gender": GENDER_MAP[app.gender],
        "Age": app.age,
        "Dependents": app.dependents,
        "Education": EDUCATION_MAP[app.education],
        "Annual_Income": app.annual_income,
        "Monthly_Expenses": app.monthly_expenses,
        "Credit_Score": app.credit_score,
        "Existing_Loans": app.existing_loans,
        "Total_Existing_Loan_Amount": app.total_existing_loan_amount,
        "Outstanding_Debt": app.outstanding_debt,
        "Loan_History": app.loan_history,
        "Loan_Amount_Requested": app.loan_amount_requested,
        "Loan_Term": app.loan_term,
        "Interest_Rate": app.interest_rate,
        "Loan_Type": LOAN_TYPE_MAP[app.loan_type],
        "Co_Applicant": CO_APPLICANT_MAP[app.co_applicant],
        "Bank_Account_History": app.bank_account_history,
        "Transaction_Frequency": app.transaction_frequency,
        # Engineered features
        "Debt_to_Income_Ratio": app.outstanding_debt / app.annual_income,
        "Loan_to_Income_Ratio": app.loan_amount_requested / app.annual_income,
        "Expense_to_Income_Ratio": (app.monthly_expenses * 12) / app.annual_income,
    }

    # One-hot encode: Marital_Status
    for val in ["Married", "Single", "Divorced"]:
        row[f"Marital_Status_{val}"] = 1 if app.marital_status == val else 0

    # One-hot encode: Employment_Status
    for val in ["Employed", "Self-Employed", "Unemployed"]:
        row[f"Employment_Status_{val}"] = 1 if app.employment_status == val else 0

    # One-hot encode: Occupation_Type
    for val in ["Business", "Freelancer", "Professional", "Salaried"]:
        row[f"Occupation_Type_{val}"] = 1 if app.occupation_type == val else 0

    # One-hot encode: Residential_Status
    for val in ["Other", "Own", "Rent"]:
        row[f"Residential_Status_{val}"] = 1 if app.residential_status == val else 0

    # One-hot encode: City_Town
    for val in ["Rural", "Suburban", "Urban"]:
        row[f"City_Town_{val}"] = 1 if app.city_town == val else 0

    # One-hot encode: Loan_Purpose
    for val in ["Education", "Home", "Personal", "Vehicle"]:
        row[f"Loan_Purpose_{val}"] = 1 if app.loan_purpose == val else 0

    return pd.DataFrame([row])
