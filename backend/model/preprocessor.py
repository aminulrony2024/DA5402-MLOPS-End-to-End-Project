"""Preprocess incoming API request to match training pipeline exactly"""
import pandas as pd
import pickle
from api.schemas.request import LoanApplication

# 🔹 Load scaler (trained during pipeline)
SCALER_PATH = "/data/features/scaler.pkl"
with open(SCALER_PATH, "rb") as f:
    scaler = pickle.load(f)

GENDER_MAP = {"Male": 1, "Female": 0}
LOAN_TYPE_MAP = {"Secured": 1, "Unsecured": 0}
CO_APPLICANT_MAP = {"Yes": 1, "No": 0}
EDUCATION_MAP = {"High School": 0, "Graduate": 1, "Postgraduate": 2}

# This exact column order must match what the model was trained on
FINAL_COLUMNS = [
    "Gender", "Age", "Dependents", "Education",
    "Annual_Income", "Monthly_Expenses", "Credit_Score",
    "Existing_Loans", "Total_Existing_Loan_Amount", "Outstanding_Debt",
    "Loan_History", "Loan_Amount_Requested", "Loan_Term",
    "Interest_Rate", "Loan_Type", "Co_Applicant",
    "Bank_Account_History", "Transaction_Frequency",
    "Debt_to_Income_Ratio", "Loan_to_Income_Ratio", "Expense_to_Income_Ratio",
    "Marital_Status_Divorced", "Marital_Status_Married", "Marital_Status_Single",
    "Employment_Status_Employed", "Employment_Status_Self-Employed", "Employment_Status_Unemployed",
    "Occupation_Type_Business", "Occupation_Type_Freelancer", "Occupation_Type_Professional", "Occupation_Type_Salaried",
    "Residential_Status_Other", "Residential_Status_Own", "Residential_Status_Rent",
    "City_Town_Rural", "City_Town_Suburban", "City_Town_Urban",
    "Loan_Purpose_Education", "Loan_Purpose_Home", "Loan_Purpose_Personal", "Loan_Purpose_Vehicle",
]

# 🔹 These columns were scaled during training
NUM_COLS = [
    "Age", "Annual_Income", "Monthly_Expenses", "Credit_Score",
    "Total_Existing_Loan_Amount", "Outstanding_Debt",
    "Loan_Amount_Requested", "Loan_Term", "Interest_Rate",
    "Bank_Account_History", "Transaction_Frequency",
    "Debt_to_Income_Ratio", "Loan_to_Income_Ratio", "Expense_to_Income_Ratio"
]


def preprocess_input(app: LoanApplication) -> pd.DataFrame:
    row = {
        # Numeric features
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

        # One-hot encoding
        "Marital_Status_Divorced": 1 if app.marital_status == "Divorced" else 0,
        "Marital_Status_Married":  1 if app.marital_status == "Married" else 0,
        "Marital_Status_Single":   1 if app.marital_status == "Single" else 0,

        "Employment_Status_Employed":      1 if app.employment_status == "Employed" else 0,
        "Employment_Status_Self-Employed": 1 if app.employment_status == "Self-Employed" else 0,
        "Employment_Status_Unemployed":    1 if app.employment_status == "Unemployed" else 0,

        "Occupation_Type_Business":    1 if app.occupation_type == "Business" else 0,
        "Occupation_Type_Freelancer":  1 if app.occupation_type == "Freelancer" else 0,
        "Occupation_Type_Professional":1 if app.occupation_type == "Professional" else 0,
        "Occupation_Type_Salaried":    1 if app.occupation_type == "Salaried" else 0,

        "Residential_Status_Other": 1 if app.residential_status == "Other" else 0,
        "Residential_Status_Own":   1 if app.residential_status == "Own" else 0,
        "Residential_Status_Rent":  1 if app.residential_status == "Rent" else 0,

        "City_Town_Rural":    1 if app.city_town == "Rural" else 0,
        "City_Town_Suburban": 1 if app.city_town == "Suburban" else 0,
        "City_Town_Urban":    1 if app.city_town == "Urban" else 0,

        "Loan_Purpose_Education": 1 if app.loan_purpose == "Education" else 0,
        "Loan_Purpose_Home":      1 if app.loan_purpose == "Home" else 0,
        "Loan_Purpose_Personal":  1 if app.loan_purpose == "Personal" else 0,
        "Loan_Purpose_Vehicle":   1 if app.loan_purpose == "Vehicle" else 0,
    }

    # Create DataFrame in correct column order
    df = pd.DataFrame([row])[FINAL_COLUMNS]

    df[NUM_COLS] = scaler.transform(df[NUM_COLS])

    return df