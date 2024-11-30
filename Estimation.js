import React, { useState } from "react";
import axios from "axios";

const Estimation = () => {
  const [formData, setFormData] = useState({
    customer_id: "",
    jobcard_id: "",
    estimation_parts: [{ part_id: "", quantity: "" }],
    service_cost: "",
    discount: "",
    tax: "",
  });
  const [message, setMessage] = useState("");

  const handleChange = (e, index) => {
    const { name, value } = e.target;
    const updatedFormData = { ...formData };

    if (name.startsWith("part_id")) {
      updatedFormData.estimation_parts[index].part_id = value;
    } else if (name.startsWith("quantity")) {
      updatedFormData.estimation_parts[index].quantity = value;
    } else {
      updatedFormData[name] = value;
    }

    setFormData(updatedFormData);
  };

  const handleAddPart = () => {
    const updatedFormData = { ...formData };
    updatedFormData.estimation_parts.push({ part_id: "", quantity: 1 });
    setFormData(updatedFormData);
  };

  const handleDeletePart = (index) => {
    const updatedFormData = { ...formData };
    updatedFormData.estimation_parts.splice(index, 1);
    setFormData(updatedFormData);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
  
    // Ensure all inputs are properly formatted
    const formattedData = {
      customer_id: parseInt(formData.customer_id, 10), // Convert to integer
      jobcard_id: parseInt(formData.jobcard_id, 10),  // Convert to integer
      estimation_parts: formData.estimation_parts.map((part) => ({
        part_id: part.part_id,                 // Keep as string (if `_id` is string in database)
        quantity: parseInt(part.quantity, 10), // Convert quantity to integer
      })),
      service_cost: parseFloat(formData.service_cost), // Convert to float
      discount: parseFloat(formData.discount),        // Convert to float
      tax: parseFloat(formData.tax),                  // Convert to float
    };
  
    console.log("Formatted data being sent:", formattedData);
  
    try {
      const response = await axios.post("http://127.0.0.1:5000/estimation", formattedData, {
        headers: {
          "Content-Type": "application/json",
        },
      });
      setMessage(response.data.message);
      // Reset the form
      setFormData({
        customer_id: "",
        jobcard_id: "",
        estimation_parts: [{ part_id: "", quantity: "" }],
        service_cost: "",
        discount: "",
        tax: "",
      });
    } catch (error) {
      console.error("Error during API call:", error);
      setMessage(error.response?.data?.error || "An error occurred. Please try again.");
    }
  };
  
  

  return (
    <div className="estimation">
      <h2>Add Estimation</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="customer_id"
          placeholder="Customer ID"
          value={formData.customer_id}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="jobcard_id"
          placeholder="Job Card ID"
          value={formData.jobcard_id}
          onChange={handleChange}
          required
        />

        <h3>Estimation Parts</h3>
        {formData.estimation_parts.map((part, index) => (
          <div key={index}>
            <input
              type="text"
              name={`part_id${index}`}
              placeholder={`Part ID ${index + 1}`}
              value={part.part_id}
              onChange={(e) => handleChange(e, index)}
              required
            />
            <input
              type="number"
              name={`quantity${index}`}
              placeholder={`Quantity ${index + 1}`}
              value={part.quantity}
              onChange={(e) => handleChange(e, index)}
              required
            />
            <button type="button" onClick={() => handleDeletePart(index)}>
              Delete Part
            </button>
          </div>
        ))}

        <button type="button" onClick={handleAddPart}>
          Add Part
        </button>

        <input
          type="number"
          name="service_cost"
          placeholder="Service Cost"
          value={formData.service_cost}
          onChange={handleChange}
          required
        />
        <input
          type="number"
          name="discount"
          placeholder="Discount"
          value={formData.discount}
          onChange={handleChange}
          required
        />
        <input
          type="number"
          name="tax"
          placeholder="Tax"
          value={formData.tax}
          onChange={handleChange}
          required
        />

        <button type="submit">Submit Estimation</button>
      </form>
      <p>{message}</p>
    </div>
  );
};

export default Estimation;
