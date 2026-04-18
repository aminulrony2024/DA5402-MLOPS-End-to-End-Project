import React from 'react';

export default function ResultCard({ result }) {
  const approved = result.loan_approved;
  const pct = (result.approval_probability * 100).toFixed(1);

  return (
    <div className={`result-card ${approved ? 'approved' : 'rejected'}`}>
      <div className="result-icon">{approved ? '✅' : '❌'}</div>
      <h2 className="result-title">{result.message}</h2>

      <div className="result-details">
        <div className="result-row">
          <span className="result-label">Approval Probability</span>
          <span className="result-value">{pct}%</span>
        </div>
        <div className="probability-bar">
          <div className="bar-fill" style={{ width: `${pct}%`, background: approved ? '#48bb78' : '#fc8181' }} />
        </div>
        <div className="result-row">
          <span className="result-label">Risk Level</span>
          <span className={`risk-badge risk-${result.risk_level.toLowerCase()}`}>{result.risk_level}</span>
        </div>
        <div className="result-row">
          <span className="result-label">Credit Score Impact</span>
          <span className="result-value">{result.credit_score_impact}</span>
        </div>
        <div className="recommendation">
          <strong>Recommendation:</strong> {result.recommendation}
        </div>
      </div>
    </div>
  );
}
