import React, { useState } from "react";
import axios from "axios";

const Employee = () => {
  const [formData, setFormData] = useState({
    name: "",
    mobile_number: "",
    alternate_number: "",
    aadhar_number: "",
    ifsc_code: "",
    pan_number: "",
    bank_account_number: "",
    address: "",
  });

  const [message, setMessage] = useState("");

  // Handle input changes
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:5000/employee", formData);
      setMessage(`Employee created successfully with ID: ${response.data.employee_id}`);
      setFormData({
        name: "",
        mobile_number: "",
        alternate_number: "",
        aadhar_number: "",
        ifsc_code: "",
        pan_number: "",
        bank_account_number: "",
        address: "",
      });
    } catch (error) {
      setMessage(error.response?.data?.error || "An error occurred. Please try again.");
    }
  };

  return (
    <div className="employee">
      <h2>Create Employee</h2>
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
          name="alternate_number"
          placeholder="Alternate Number"
          value={formData.alternate_number}
          onChange={handleChange}
        />
        <input
          type="text"
          name="aadhar_number"
          placeholder="Aadhar Number"
          value={formData.aadhar_number}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="ifsc_code"
          placeholder="IFSC Code"
          value={formData.ifsc_code}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="pan_number"
          placeholder="PAN Number"
          value={formData.pan_number}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="bank_account_number"
          placeholder="Bank Account Number"
          value={formData.bank_account_number}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="address"
          placeholder="Address"
          value={formData.address}
          onChange={handleChange}
          required
        />
        <button type="submit">Create Employee</button>
      </form>
      <p>{message}</p>
    </div>
  );
};

export default Employee;
