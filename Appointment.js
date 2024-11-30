import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import "./Dashboard.css"; // Reuse the same CSS from Dashboard

const Appointment = ({ isAuthenticated, onLogout }) => {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    name: "",
    mobile_number: "",
    alternative_number: "",
    address: "",
    car_number: "",
    email: "",
  });
  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:5000/appointment", formData);
      setMessage(response.data.message);
      setFormData({
        name: "",
        mobile_number: "",
        alternative_number: "",
        address: "",
        car_number: "",
        email: "",
      });
    } catch (error) {
      setMessage(error.response?.data?.error || "Error submitting the form");
    }
  };

  const handleLogout = () => {
    onLogout();
    navigate("/login");
  };

  return (
    <div className="dashboard">
     
      {/* Main Content */}
      <div className="content">
        <h2>Book an Appointment</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            name="name"
            placeholder="Name"
            value={formData.name}
            onChange={handleChange}
            required
          />
          <input
            type="text"
            name="mobile_number"
            placeholder="Mobile Number"
            value={formData.mobile_number}
            onChange={handleChange}
            required
          />
          <input
            type="text"
            name="alternative_number"
            placeholder="Alternative Number"
            value={formData.alternative_number}
            onChange={handleChange}
          />
          <input
            type="text"
            name="address"
            placeholder="Address"
            value={formData.address}
            onChange={handleChange}
            required
          />
          <input
            type="text"
            name="car_number"
            placeholder="Car Number"
            value={formData.car_number}
            onChange={handleChange}
            required
          />
          <input
            type="email"
            name="email"
            placeholder="Email"
            value={formData.email}
            onChange={handleChange}
            required
          />
          <button type="submit">Submit Appointment</button>
        </form>
        <p>{message}</p>
      </div>
    </div>
  );
};

export default Appointment;
