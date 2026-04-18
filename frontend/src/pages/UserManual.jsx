import React from 'react';

export default function UserManual() {
  return (
    <div className="manual-page">
      <div className="page-header">
        <h1>User Manual</h1>
        <p>How to use the FinPredict Loan Approval System</p>
      </div>

      <div className="manual-section">
        <h2>What is FinPredict?</h2>
        <p>
          FinPredict is an AI-powered system that instantly predicts whether your
          loan application is likely to be approved or rejected, based on your
          financial profile and loan details.
        </p>
      </div>

      <div className="manual-section">
        <h2>How to Check Loan Eligibility</h2>
        <ol>
          <li>Click on <strong>Apply</strong> in the navigation bar at the top.</li>
          <li>Fill in your <strong>Personal Details</strong> — Gender, Age, Marital Status, Dependents, Education.</li>
          <li>Fill in your <strong>Employment Details</strong> — Job type, Residential status, City.</li>
          <li>Fill in your <strong>Financial Details</strong> — Income, Expenses, Credit Score, Existing Loans, Debt.</li>
          <li>Fill in your <strong>Loan Details</strong> — Amount, Term, Purpose, Interest Rate, Type.</li>
          <li>Click the <strong>"Check Loan Eligibility"</strong> button.</li>
          <li>View your result instantly.</li>
        </ol>
      </div>

      <div className="manual-section">
        <h2>Understanding Your Result</h2>
        <ul>
          <li><strong>Loan Approved</strong> — Your profile meets the criteria for loan approval.</li>
          <li><strong>Loan Rejected</strong> — Your application may not be approved based on current data.</li>
          <li><strong>Approval Probability</strong> — A percentage showing how confident the AI is.</li>
          <li><strong>Risk Level</strong> — Low / Medium / High risk classification of your profile.</li>
          <li><strong>Credit Score Impact</strong> — How your credit score affects the decision.</li>
          <li><strong>Recommendation</strong> — Tips to improve your approval chances.</li>
        </ul>
      </div>

      <div className="manual-section">
        <h2>Tips to Improve Your Chances</h2>
        <ul>
          <li>Maintain a credit score above 700</li>
          <li>Keep your outstanding debt low relative to your income</li>
          <li>Reduce your monthly expenses where possible</li>
          <li>Apply for a loan amount proportional to your annual income</li>
          <li>Having a co-applicant can improve your chances</li>
        </ul>
      </div>
    </div>
  );
}
