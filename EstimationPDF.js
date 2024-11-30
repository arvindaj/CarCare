import React, { useState } from "react";
import axios from "axios";

const EstimationPDF = () => {
  const [estimationId, setEstimationId] = useState("");
  const [estimationData, setEstimationData] = useState(null);
  const [message, setMessage] = useState("");

  // Handle input change
  const handleChange = (e) => {
    setEstimationId(e.target.value);
  };

  // Fetch estimation details
  const fetchEstimation = async () => {
    try {
      const response = await axios.get(`http://127.0.0.1:5000/estimation/${estimationId}`);
      const data = response.data.estimation;
      setEstimationData(JSON.parse(data));
      setMessage("Estimation details fetched successfully.");
    } catch (error) {
      setMessage(error.response?.data?.error || "Error fetching estimation details.");
      setEstimationData(null);
    }
  };

  // Send estimation PDF
  const sendEstimationPDF = async () => {
    try {
      const response = await axios.post(`http://127.0.0.1:5000/send_estimation_pdf/${estimationId}`);
      setMessage(response.data.message || "PDF sent successfully to the customer's email.");
    } catch (error) {
      setMessage(error.response?.data?.error || "Error sending PDF.");
    }
  };

  return (
    <div className="estimation-pdf">
      <h2>Estimation PDF System</h2>

      {/* Input for Estimation ID */}
      <input
        type="text"
        placeholder="Enter Estimation ID"
        value={estimationId}
        onChange={handleChange}
      />
      <button onClick={fetchEstimation}>Fetch Estimation</button>
      <button onClick={sendEstimationPDF} disabled={!estimationId}>
        Send Estimation PDF
      </button>

      {/* Message Section */}
      {message && <p>{message}</p>}

      {/* Estimation Details */}
      {estimationData && (
        <div className="estimation-details">
          <h3>Estimation Details</h3>
          <pre>{JSON.stringify(estimationData, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default EstimationPDF;
