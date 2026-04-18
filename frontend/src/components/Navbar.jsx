import React from 'react';
import { Link } from 'react-router-dom';

export default function Navbar() {
  return (
    <nav className="navbar">
      <div className="nav-brand">FinPredict</div>
      <div className="nav-links">
        <Link to="/">Home</Link>
        <Link to="/predict">Apply</Link>
        <Link to="/pipeline">Pipeline</Link>
        <Link to="/manual">User Manual</Link>
      </div>
    </nav>
  );
}
