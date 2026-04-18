"""Input schema for loan application"""
from pydantic import BaseModel, Field
from typing import Literal


class LoanApplication(BaseModel):
    gender: Literal["Male", "Female"]
    age: int = Field(..., ge=18, le=100)
    marital_status: Literal["Married", "Single", "Divorced"]
    dependents: int = Field(..., ge=0, le=10)
    education: Literal["Graduate", "High School", "Postgraduate"]
    employment_status: Literal["Employed", "Self-Employed", "Unemployed"]
    occupation_type: Literal["Professional", "Salaried", "Freelancer", "Business"]
    residential_status: Literal["Own", "Rent", "Other"]
    city_town: Literal["Urban", "Suburban", "Rural"]
    annual_income: float = Field(..., gt=0)
    monthly_expenses: float = Field(..., gt=0)
    credit_score: int = Field(..., ge=300, le=850)
    existing_loans: int = Field(..., ge=0)
    total_existing_loan_amount: float = Field(..., ge=0)
    outstanding_debt: float = Field(..., ge=0)
    loan_history: int = Field(..., ge=0, le=1)
    loan_amount_requested: float = Field(..., gt=0)
    loan_term: int = Field(..., gt=0)
    loan_purpose: Literal["Home", "Personal", "Vehicle", "Education"]
    interest_rate: float = Field(..., gt=0)
    loan_type: Literal["Secured", "Unsecured"]
    co_applicant: Literal["Yes", "No"]
    bank_account_history: int = Field(..., ge=0)
    transaction_frequency: int = Field(..., ge=0)

    class Config:
        json_schema_extra = {
            "example": {
                "gender": "Male", "age": 35, "marital_status": "Married",
                "dependents": 1, "education": "Graduate",
                "employment_status": "Employed", "occupation_type": "Salaried",
                "residential_status": "Own", "city_town": "Urban",
                "annual_income": 85000, "monthly_expenses": 2500,
                "credit_score": 720, "existing_loans": 1,
                "total_existing_loan_amount": 15000, "outstanding_debt": 8000,
                "loan_history": 0, "loan_amount_requested": 20000,
                "loan_term": 120, "loan_purpose": "Home",
                "interest_rate": 8.5, "loan_type": "Secured",
                "co_applicant": "Yes", "bank_account_history": 5,
                "transaction_frequency": 15
            }
        }
