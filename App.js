import React, { useState } from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import Login from "./components/Login";
import Register from "./components/Register";
import AdminLogin from "./components/AdminLogin";
import Appointment from "./components/Appointment";
import Estimation from "./components/Estimation";
import JobCard from "./components/JobCard";
import Employee from "./components/Employee";
import Stock from "./components/Stock";
import EstimationPDF from "./components/EstimationPDF";
import Dashboard from "./components/Dashboard";
import Layout from "./components/Layout";
import NewPut from "./components/Newput";

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Handle login state
  const handleLogin = (status) => {
    setIsAuthenticated(status);
  };

  // Handle logout state
  const handleLogout = () => {
    setIsAuthenticated(false);
  };

  // Component for protecting routes
  const ProtectedRoute = ({ element }) => {
    return isAuthenticated ? element : <Navigate to="/login" replace />;
  };

  return (
    <Router>
      <div className="app">
        <Routes>
          {/* Login and Register Routes */}
          <Route
            path="/login"
            element={<Login onLogin={(status) => handleLogin(status)} />}
          />
          <Route path="/register" element={<Register />} />
          <Route
            path="/admin-login"
            element={<AdminLogin onLogin={(status) => handleLogin(status)} />}
          />

          {/* Protected Routes with Sidebar */}
          <Route
            path="/"
            element={
              <ProtectedRoute
                element={
                  <Layout isAuthenticated={isAuthenticated} onLogout={handleLogout} />
                }
              />
            }
          >
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/appointment" element={<Appointment />} />
            <Route path="/estimation" element={<Estimation />} />
            <Route path="/jobcard" element={<JobCard />} />
            <Route path="/employee" element={<Employee />} />
            <Route path="/stock" element={<Stock />} />
            <Route path="/estimationpdf" element={<EstimationPDF />} />
            <Route path="/newput" element={<NewPut/>}/>
          </Route>

          {/* Redirect for unknown routes */}
          <Route
            path="*"
            element={
              isAuthenticated ? <Navigate to="/dashboard" /> : <Navigate to="/login" />
            }
          />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
