import React, { useState } from "react";
import axios from "axios";

const Stock = () => {
  const [formData, setFormData] = useState({
    name: "",
    unit_price: "",
    discount: "",
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

    // Convert unit_price and discount to integers
    const dataToSend = {
      ...formData,
      unit_price: parseInt(formData.unit_price, 10),
      discount: parseInt(formData.discount, 10),
    };

    try {
      const response = await axios.post("http://127.0.0.1:5000/add-part", dataToSend);
      setMessage(response.data.message || "Stock added successfully!");
      setFormData({
        name: "",
        unit_price: "",
        discount: "",
      });
    } catch (error) {
      setMessage(error.response?.data?.error || "An error occurred. Please try again.");
    }
  };

  return (
    <div className="stock">
      <h2>Add New Stock</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="name"
          placeholder="Item Name"
          value={formData.name}
          onChange={handleChange}
          required
        />
        <input
          type="number"
          name="unit_price"
          placeholder="Unit Price"
          value={formData.unit_price}
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
        <button type="submit">Add Stock</button>
      </form>
      <p>{message}</p>
    </div>
  );
};

export default Stock;
