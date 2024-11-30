import React, { useState } from "react";
import axios from "axios";

const JobCard = () => {
  const [formData, setFormData] = useState({
    employee_id: "",
    customer_id: "",
    service_type: "",
    labour_cost: "",
    car_model: "",
    car_make: "",
    year: "",
    fuel_type: "",
    vehicle_colour: "",
    chasse_number: "",
    estimation_delivery_date: "",
    insurance_company: "",
    advance_payment: "",
    car_image: "",
  });

  const [message, setMessage] = useState("");

  // Handle input changes and ensure advance_payment is an integer
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevFormData) => {
      if (name === "advance_payment") {
        // Convert to integer if it's the advance_payment field
        return {
          ...prevFormData,
          [name]: value ? parseInt(value) : "", // Ensure it's an integer
        };
      } else if (name === "customer_id") {
        // Convert customer_id to integer as well
        return {
          ...prevFormData,
          [name]: value ? parseInt(value) : "", // Ensure it's an integer
        };
      }
      return {
        ...prevFormData,
        [name]: value,
      };
    });
  };

  // Submit the form and send data to the backend
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:5000/api/job_card", formData);
      setMessage(response.data.message);
      // Reset the form after successful submission
      setFormData({
        employee_id: "",
        customer_id: "",
        service_type: "",
        labour_cost: "",
        car_model: "",
        car_make: "",
        year: "",
        fuel_type: "",
        vehicle_colour: "",
        chasse_number: "",
        estimation_delivery_date: "",
        insurance_company: "",
        advance_payment: "",
        car_image: "",
      });
    } catch (error) {
      setMessage(error.response?.data?.error || "An error occurred. Please try again.");
    }
  };

  return (
    <div className="job-card">
      <h2>Create Job Card</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="employee_id"
          placeholder="Employee ID"
          value={formData.employee_id}
          onChange={handleChange}
          required
        />
        <input
          type="number"
          name="customer_id"
          placeholder="Customer ID"
          value={formData.customer_id}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="service_type"
          placeholder="Service Type"
          value={formData.service_type}
          onChange={handleChange}
          required
        />
        <input
          type="number"
          name="labour_cost"
          placeholder="Labour Cost"
          value={formData.labour_cost}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="car_model"
          placeholder="Car Model"
          value={formData.car_model}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="car_make"
          placeholder="Car Make"
          value={formData.car_make}
          onChange={handleChange}
          required
        />
        <input
          type="number"
          name="year"
          placeholder="Year"
          value={formData.year}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="fuel_type"
          placeholder="Fuel Type"
          value={formData.fuel_type}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="vehicle_colour"
          placeholder="Vehicle Colour"
          value={formData.vehicle_colour}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="chasse_number"
          placeholder="Chassis Number"
          value={formData.chasse_number}
          onChange={handleChange}
          required
        />
        <input
          type="date"
          name="estimation_delivery_date"
          placeholder="Estimation Delivery Date"
          value={formData.estimation_delivery_date}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="insurance_company"
          placeholder="Insurance Company"
          value={formData.insurance_company}
          onChange={handleChange}
        />
        <input
          type="number"
          name="advance_payment"
          placeholder="Advance Payment"
          value={formData.advance_payment}
          onChange={handleChange}
        />
        <input
          type="url"
          name="car_image"
          placeholder="Car Image URL"
          value={formData.car_image}
          onChange={handleChange}
        />
        <button type="submit">Create Job Card</button>
      </form>
      <p>{message}</p>
    </div>
  );
};

export default JobCard;
