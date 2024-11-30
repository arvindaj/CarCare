import React from "react";
import { Link, Outlet } from "react-router-dom";
import "./Dashboard.css"; // Add shared styles for sidebar

const Layout = ({ isAuthenticated, onLogout }) => {
  return (
    <div className="dashboard">
      <div className="sidebar">
        <nav className="nav-links">
          <h2>Dashboard</h2>
          <ul>
            <li>
              <Link to="/dashboard">Home</Link>
            </li>
            <li>
              <Link to="/appointment">Book Appointment</Link>
            </li>
            <li>
              <Link to="/estimation">Estimation</Link>
            </li>
            <li>
              <Link to="/jobcard">Job Card</Link>
            </li>
            <li>
              <Link to="/employee">Employee</Link>
            </li>
            <li>
              <Link to="/stock">Stock</Link>
            </li>
            <li>
              <Link to="/estimationpdf">Generate Estimation PDF</Link>
            </li>
            <li>
              <Link to="/newput">newput</Link>
            </li>
          </ul>
        </nav>
        <div className="auth-buttons">
          <button onClick={onLogout}>{isAuthenticated ? "Logout" : "Login"}</button>
        </div>
      </div>
      <div className="content">
        <Outlet /> {/* Renders the current route's component */}
      </div>
    </div>
  );
};

export default Layout;
