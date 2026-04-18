import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Predict from './pages/Predict';
import Pipeline from './pages/Pipeline';
import UserManual from './pages/UserManual';

export default function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/predict" element={<Predict />} />
        <Route path="/pipeline" element={<Pipeline />} />
        <Route path="/manual" element={<UserManual />} />
      </Routes>
    </Router>
  );
}
