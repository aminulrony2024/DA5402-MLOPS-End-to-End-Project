import React, { useState } from 'react';
import { predictLoan } from '../api/apiClient';
import ResultCard from './ResultCard';
import Loader from './Loader';

const INITIAL_FORM = {
  gender: 'Male', age: '', marital_status: 'Married',
  dependents: '', education: 'Graduate',
  employment_status: 'Employed', occupation_type: 'Salaried',
  residential_status: 'Own', city_town: 'Urban',
  annual_income: '', monthly_expenses: '', credit_score: '',
  existing_loans: '', total_existing_loan_amount: '',
  outstanding_debt: '', loan_history: '0',
  loan_amount_requested: '', loan_term: '',
  loan_purpose: 'Home', interest_rate: '',
  loan_type: 'Secured', co_applicant: 'No',
  bank_account_history: '', transaction_frequency: ''
};

export default function LoanForm() {
  const [form, setForm] = useState(INITIAL_FORM);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setForm(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const payload = {
        ...form,
        age: parseInt(form.age),
        dependents: parseInt(form.dependents),
        annual_income: parseFloat(form.annual_income),
        monthly_expenses: parseFloat(form.monthly_expenses),
        credit_score: parseInt(form.credit_score),
        existing_loans: parseInt(form.existing_loans),
        total_existing_loan_amount: parseFloat(form.total_existing_loan_amount),
        outstanding_debt: parseFloat(form.outstanding_debt),
        loan_history: parseInt(form.loan_history),
        loan_amount_requested: parseFloat(form.loan_amount_requested),
        loan_term: parseInt(form.loan_term),
        interest_rate: parseFloat(form.interest_rate),
        bank_account_history: parseInt(form.bank_account_history),
        transaction_frequency: parseInt(form.transaction_frequency),
      };
      const prediction = await predictLoan(payload);
      setResult(prediction);
    } catch (err) {
      setError('Prediction failed. Please check your inputs and try again.');
    }
    setLoading(false);
  };

  return (
    <div className="form-container">
      <h2 className="form-title">Loan Application Form</h2>

      <div className="form-grid">

        {/* ── PERSONAL DETAILS ── */}
        <div className="form-section">
          <h3 className="section-title">Personal Details</h3>

          <label className="form-label">Gender
            <select name="gender" value={form.gender} onChange={handleChange} className="form-input">
              <option>Male</option>
              <option>Female</option>
            </select>
          </label>

          <label className="form-label">Age
            <input name="age" type="number" value={form.age}
              onChange={handleChange} className="form-input" placeholder="e.g. 30" />
          </label>

          <label className="form-label">Marital Status
            <select name="marital_status" value={form.marital_status} onChange={handleChange} className="form-input">
              <option>Married</option>
              <option>Single</option>
              <option>Divorced</option>
            </select>
          </label>

          <label className="form-label">Dependents
            <input name="dependents" type="number" value={form.dependents}
              onChange={handleChange} className="form-input" placeholder="e.g. 2" />
          </label>

          <label className="form-label">Education
            <select name="education" value={form.education} onChange={handleChange} className="form-input">
              <option>Graduate</option>
              <option>High School</option>
              <option>Postgraduate</option>
            </select>
          </label>
        </div>

        {/* ── EMPLOYMENT DETAILS ── */}
        <div className="form-section">
          <h3 className="section-title">Employment Details</h3>

          <label className="form-label">Employment Status
            <select name="employment_status" value={form.employment_status} onChange={handleChange} className="form-input">
              <option>Employed</option>
              <option>Self-Employed</option>
              <option>Unemployed</option>
            </select>
          </label>

          <label className="form-label">Occupation Type
            <select name="occupation_type" value={form.occupation_type} onChange={handleChange} className="form-input">
              <option>Salaried</option>
              <option>Professional</option>
              <option>Freelancer</option>
              <option>Business</option>
            </select>
          </label>

          <label className="form-label">Residential Status
            <select name="residential_status" value={form.residential_status} onChange={handleChange} className="form-input">
              <option>Own</option>
              <option>Rent</option>
              <option>Other</option>
            </select>
          </label>

          <label className="form-label">City / Town
            <select name="city_town" value={form.city_town} onChange={handleChange} className="form-input">
              <option>Urban</option>
              <option>Suburban</option>
              <option>Rural</option>
            </select>
          </label>

          <label className="form-label">Co-Applicant
            <select name="co_applicant" value={form.co_applicant} onChange={handleChange} className="form-input">
              <option>No</option>
              <option>Yes</option>
            </select>
          </label>
        </div>

        {/* ── FINANCIAL DETAILS ── */}
        <div className="form-section">
          <h3 className="section-title">Financial Details</h3>

          <label className="form-label">Annual Income
            <input name="annual_income" type="text" value={form.annual_income}
              onChange={handleChange} className="form-input" placeholder="e.g. 85000" />
          </label>

          <label className="form-label">Monthly Expenses
            <input name="monthly_expenses" type="text" value={form.monthly_expenses}
              onChange={handleChange} className="form-input" placeholder="e.g. 2500" />
          </label>

          <label className="form-label">Credit Score (300–850)
            <input name="credit_score" type="text" value={form.credit_score}
              onChange={handleChange} className="form-input" placeholder="e.g. 720" />
          </label>

          <label className="form-label">Existing Loans
            <input name="existing_loans" type="text" value={form.existing_loans}
              onChange={handleChange} className="form-input" placeholder="e.g. 1" />
          </label>

          <label className="form-label">Total Existing Loan Amount
            <input name="total_existing_loan_amount" type="text" value={form.total_existing_loan_amount}
              onChange={handleChange} className="form-input" placeholder="e.g. 15000" />
          </label>

          <label className="form-label">Outstanding Debt
            <input name="outstanding_debt" type="text" value={form.outstanding_debt}
              onChange={handleChange} className="form-input" placeholder="e.g. 8000" />
          </label>

          <label className="form-label">Loan History
            <select name="loan_history" value={form.loan_history} onChange={handleChange} className="form-input">
              <option value="0">No Previous Loan</option>
              <option value="1">Has Previous Loan</option>
            </select>
          </label>

          <label className="form-label">Bank Account History (years)
            <input name="bank_account_history" type="number" value={form.bank_account_history}
              onChange={handleChange} className="form-input" placeholder="e.g. 5" />
          </label>

          <label className="form-label">Transaction Frequency
            <input name="transaction_frequency" type="number" value={form.transaction_frequency}
              onChange={handleChange} className="form-input" placeholder="e.g. 15" />
          </label>
        </div>

        {/* ── LOAN DETAILS ── */}
        <div className="form-section">
          <h3 className="section-title">Loan Details</h3>

          <label className="form-label">Loan Amount Requested
            <input name="loan_amount_requested" type="text" value={form.loan_amount_requested}
              onChange={handleChange} className="form-input" placeholder="e.g. 20000" />
          </label>

          <label className="form-label">Loan Term (months)
            <input name="loan_term" type="number" value={form.loan_term}
              onChange={handleChange} className="form-input" placeholder="e.g. 120" />
          </label>

          <label className="form-label">Loan Purpose
            <select name="loan_purpose" value={form.loan_purpose} onChange={handleChange} className="form-input">
              <option>Home</option>
              <option>Personal</option>
              <option>Vehicle</option>
              <option>Education</option>
            </select>
          </label>

          <label className="form-label">Interest Rate (%)
            <input name="interest_rate" type="number" step="0.01" value={form.interest_rate}
              onChange={handleChange} className="form-input" placeholder="e.g. 8.5" />
          </label>

          <label className="form-label">Loan Type
            <select name="loan_type" value={form.loan_type} onChange={handleChange} className="form-input">
              <option>Secured</option>
              <option>Unsecured</option>
            </select>
          </label>
        </div>

      </div>

      {error && <div className="error-msg">{error}</div>}

      <button className="submit-btn" onClick={handleSubmit} disabled={loading}>
        {loading ? 'Predicting...' : 'Check Loan Eligibility'}
      </button>

      {loading && <Loader />}
      {result && <ResultCard result={result} />}
    </div>
  );
}