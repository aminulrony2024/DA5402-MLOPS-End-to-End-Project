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

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);
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

  const Field = ({ label, name, type = 'number', children }) => (
    <label className="form-label">
      {label}
      {children || <input type={type} name={name} value={form[name]} onChange={handleChange} className="form-input" />}
    </label>
  );

  const Select = ({ label, name, options }) => (
    <label className="form-label">
      {label}
      <select name={name} value={form[name]} onChange={handleChange} className="form-input">
        {options.map(o => <option key={o} value={o}>{o}</option>)}
      </select>
    </label>
  );

  return (
    <div className="form-container">
      <h2 className="form-title">Loan Application Form</h2>

      <div className="form-grid">
        {/* Personal Details */}
        <div className="form-section">
          <h3 className="section-title">Personal Details</h3>
          <Select label="Gender" name="gender" options={['Male', 'Female']} />
          <Field label="Age" name="age" />
          <Select label="Marital Status" name="marital_status" options={['Married', 'Single', 'Divorced']} />
          <Field label="Dependents" name="dependents" />
          <Select label="Education" name="education" options={['Graduate', 'High School', 'Postgraduate']} />
        </div>

        {/* Employment Details */}
        <div className="form-section">
          <h3 className="section-title">Employment Details</h3>
          <Select label="Employment Status" name="employment_status" options={['Employed', 'Self-Employed', 'Unemployed']} />
          <Select label="Occupation Type" name="occupation_type" options={['Salaried', 'Professional', 'Freelancer', 'Business']} />
          <Select label="Residential Status" name="residential_status" options={['Own', 'Rent', 'Other']} />
          <Select label="City / Town" name="city_town" options={['Urban', 'Suburban', 'Rural']} />
          <Select label="Co-Applicant" name="co_applicant" options={['No', 'Yes']} />
        </div>

        {/* Financial Details */}
        <div className="form-section">
          <h3 className="section-title">Financial Details</h3>
          <Field label="Annual Income" name="annual_income" />
          <Field label="Monthly Expenses" name="monthly_expenses" />
          <Field label="Credit Score (300–850)" name="credit_score" />
          <Field label="Existing Loans" name="existing_loans" />
          <Field label="Total Existing Loan Amount" name="total_existing_loan_amount" />
          <Field label="Outstanding Debt" name="outstanding_debt" />
          <Select label="Loan History" name="loan_history" options={['0', '1']}>
            <select name="loan_history" value={form.loan_history} onChange={handleChange} className="form-input">
              <option value="0">No Previous Loan</option>
              <option value="1">Has Previous Loan</option>
            </select>
          </Select>
          <Field label="Bank Account History (years)" name="bank_account_history" />
          <Field label="Transaction Frequency" name="transaction_frequency" />
        </div>

        {/* Loan Details */}
        <div className="form-section">
          <h3 className="section-title">Loan Details</h3>
          <Field label="Loan Amount Requested" name="loan_amount_requested" />
          <Field label="Loan Term (months)" name="loan_term" />
          <Select label="Loan Purpose" name="loan_purpose" options={['Home', 'Personal', 'Vehicle', 'Education']} />
          <Field label="Interest Rate (%)" name="interest_rate" type="number" />
          <Select label="Loan Type" name="loan_type" options={['Secured', 'Unsecured']} />
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
