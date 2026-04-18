import React from 'react';
import { Link } from 'react-router-dom';

export default function Home() {
  return (
    <div className="home-page">
      <div className="hero">
        <h1>FinPredict</h1>
        <p className="hero-sub">Intelligent Loan Approval System powered by AI</p>
        <Link to="/predict" className="cta-btn">Check Your Eligibility</Link>
      </div>

      <div className="features">
        <div className="feature-card">
          <div className="feature-icon">⚡</div>
          <h3>Instant Decision</h3>
          <p>Get loan approval predictions in under a second</p>
        </div>
        <div className="feature-card">
          <div className="feature-icon">🤖</div>
          <h3>AI Powered</h3>
          <p>XGBoost model trained on 52,000+ real records</p>
        </div>
        <div className="feature-card">
          <div className="feature-icon">📊</div>
          <h3>Transparent</h3>
          <p>Understand why your loan was approved or rejected</p>
        </div>
        <div className="feature-card">
          <div className="feature-icon">🔒</div>
          <h3>Secure</h3>
          <p>Your data is processed securely and never stored</p>
        </div>
      </div>
    </div>
  );
}
