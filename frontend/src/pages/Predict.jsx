import React from 'react';
import LoanForm from '../components/LoanForm';

export default function Predict() {
  return (
    <div className="predict-page">
      <div className="page-header">
        <h1>Loan Eligibility Check</h1>
        <p>Fill in your details below to instantly check if your loan will be approved.</p>
      </div>
      <LoanForm />
    </div>
  );
}
