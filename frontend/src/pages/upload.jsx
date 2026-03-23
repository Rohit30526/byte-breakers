import "../styles/upload.css";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Upload() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  // Select file
  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setMessage("");
    }
  };

  // Upload + move to selfie
  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file first");
      return;
    }

    // ✅ Store file globally (for selfie page)
    window.selectedIdFile = file;

    try {
      // (Optional) check backend connection
      const res = await fetch("http://127.0.0.1:8001/");
      const data = await res.json();

      console.log(data);
      setMessage("Backend connected ✅");

      // ✅ MOVE TO NEXT PAGE
      setTimeout(() => {
        navigate("/selfie");
      }, 800); // small delay for UX

    } catch (error) {
      console.error(error);
      setMessage("Backend connection failed ❌");
    }
  };

  return (
    <section className="upload-container">

      {/* TOP STEPS */}
      <div className="steps">
        <div className="step active">1. ID Verification</div>
        <div className="step">2. Face Match</div>
        <div className="step">3. KYC Result</div>
      </div>

      {/* TITLE */}
      <h2>Upload Identity Document</h2>
      <p className="subtitle">
        Please provide a clear photo of your government-issued ID
      </p>

      {/* UPLOAD BOX */}
      <div className="upload-box">

        <div className="upload-icon">⬆</div>

        <p>Drag and drop your ID here</p>
        <span>or click to browse from your device</span>

        {/* Hidden file input */}
        <input
          type="file"
          id="fileInput"
          style={{ display: "none" }}
          onChange={handleFileChange}
        />

        {/* Select button */}
        <button
          className="upload-btn"
          onClick={() => document.getElementById("fileInput").click()}
        >
          Select Document
        </button>

        {/* Upload button */}
        <button
          className="upload-btn"
          onClick={handleUpload}
        >
          Upload & Continue →
        </button>

        {/* Show file name */}
        {file && (
          <p className="file-name">
            Selected: {file.name}
          </p>
        )}

        {/* Status message */}
        {message && (
          <p className="status-msg">{message}</p>
        )}

        <div className="upload-tags">
          <span>OCR READY</span>
          <span>AUTHENTIC</span>
          <span>HIGH RES</span>
        </div>

      </div>

      {/* GUIDELINES */}
      <div className="guidelines">
        <h4>Security Guidelines</h4>
        <ul>
          <li>Ensure all four corners of the ID are visible</li>
          <li>Avoid glare and shadows on the document</li>
          <li>The text must be clearly readable</li>
          <li>Document must be valid and not expired</li>
        </ul>
      </div>

    </section>
  );
}