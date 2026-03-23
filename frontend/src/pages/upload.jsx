import { useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/upload.css";

export default function Upload() {
  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  const [file, setFile] = useState(null);
  const [error, setError] = useState("");

  const handleFile = (e) => {
    const selected = e.target.files[0];
    if (!selected) return;

    // ✅ VALIDATION
    const validTypes = ["image/jpeg", "image/png", "application/pdf"];

    if (!validTypes.includes(selected.type)) {
      setError("Only JPG, PNG, or PDF files are allowed");
      return;
    }

    if (selected.size > 5 * 1024 * 1024) {
      setError("File size must be less than 5MB");
      return;
    }

    setError("");

    // ✅ STORE FILE DATA
    setFile({
      preview: URL.createObjectURL(selected),
      name: selected.name,
      size: (selected.size / 1024 / 1024).toFixed(2),
      type: selected.type,
    });

    // 👉 AUTO MOVE TO PROCESSING (simulate)
    setTimeout(() => {
      navigate("/selfie");
    }, 1500);
  };

  return (
    <section className="upload-container">

      {/* STEP PROGRESS */}
      <div className="steps">
        <div className="step active">1. ID Verification</div>
        <div className="step">2. Face Match</div>
        <div className="step">3. KYC Result</div>
      </div>

      {/* TITLE */}
      <h2>Upload Aadhaar / ID Document</h2>
      <p className="subtitle">
        Upload a clear image of your Aadhaar card (front side)
      </p>

      {/* UPLOAD BOX */}
      <div className="upload-box">

        {!file ? (
          <>
            <div className="upload-icon">📄</div>
            <p>Drag & drop your document here</p>
            <span>Supports JPG, PNG, PDF</span>

            {/* 🔥 HIDDEN INPUT */}
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFile}
              style={{ display: "none" }}
            />

            {/* 🔥 BUTTON */}
            <button
              className="upload-btn"
              onClick={() => fileInputRef.current.click()}
            >
              Select Document
            </button>

            {error && <p className="error">{error}</p>}
          </>
        ) : (
          <div className="preview-section">
            {file.type.includes("image") ? (
              <img src={file.preview} alt="preview" />
            ) : (
              <p>📄 PDF Uploaded</p>
            )}

            <div className="file-info">
              <p><strong>{file.name}</strong></p>
              <p>{file.size} MB</p>
            </div>
          </div>
        )}

      </div>

      {/* GUIDELINES */}
      <div className="guidelines">
        <h4>Security Guidelines</h4>
        <ul>
          <li>Ensure all corners of Aadhaar are visible</li>
          <li>No blur or glare</li>
          <li>Text must be readable</li>
          <li>Use original document (no photocopy)</li>
        </ul>
      </div>

    </section>
  );
}