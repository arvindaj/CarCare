import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const Login = ({ onLogin }) => {
  const [view, setView] = useState(""); // Tracks the active form view: 'login', 'admin', or 'register'
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const endpoint =
        view === "admin" ? "http://127.0.0.1:5000/admin-login" : "http://127.0.0.1:5000/login";
      const response = await axios.post(endpoint, { username, password });
      onLogin(true); // Update auth state in App
      setMessage("Login successful!");
      const redirectPath = view === "admin" ? "/admin-dashboard" : "/appointment";
      navigate(redirectPath); // Redirect based on user type
    } catch (error) {
      setMessage(error.response?.data?.error || "Login failed!");
      onLogin(false); // Reset auth state
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      await axios.post("http://127.0.0.1:5000/register", {
        username,
        password,
      });
      setMessage("Registration successful! Please log in.");
      setView("login"); // Redirect to login form
    } catch (error) {
      setMessage(error.response?.data?.error || "Registration failed!");
    }
  };

  const handleLogout = () => {
    onLogin(false); // Reset auth state
    setUsername("");
    setPassword("");
    setMessage("Logged out successfully!");
    navigate("/login");
  };

  return (
    <div className="login">
      {!view && ( // Show buttons if no form is selected
        <div>
          <button onClick={() => setView("login")}>Login</button>
          <button onClick={() => setView("admin")}>Admin Login</button>
          <button onClick={() => setView("register")}>Register</button>
        </div>
      )}

      {view === "login" && (
        <div>
          <h2>User Login</h2>
          <form onSubmit={handleLogin}>
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <button type="submit">Login</button>
          </form>
          <button onClick={() => setView("")}>Back</button>
        </div>
      )}

      {view === "admin" && (
        <div>
          <h2>Admin Login</h2>
          <form onSubmit={handleLogin}>
            <input
              type="text"
              placeholder="Admin Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <button type="submit">Login</button>
          </form>
          <button onClick={() => setView("")}>Back</button>
        </div>
      )}

      {view === "register" && (
        <div>
          <h2>Register</h2>
          <form onSubmit={handleRegister}>
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <button type="submit">Register</button>
          </form>
          <button onClick={() => setView("")}>Back</button>
        </div>
      )}

      {onLogin && ( // Show Logout button if authenticated
        <button onClick={handleLogout} style={{ marginTop: "20px" }}>
          Logout
        </button>
      )}
      <p>{message}</p>
    </div>
  );
};

export default Login;
