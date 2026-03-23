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

    const validTypes = ["image/jpeg", "image/png", "application/pdf"];

    if (!validTypes.includes(selected.type)) {
      setError("Only JPG, PNG, or PDF allowed");
      return;
    }

    if (selected.size > 5 * 1024 * 1024) {
      setError("File must be under 5MB");
      return;
    }

    setError("");

    setFile({
      file: selected,
      name: selected.name,
      preview: URL.createObjectURL(selected),
      type: selected.type,
    });
  };

  return (
    <section className="upload-container">

      {/* STEPS */}
      <div className="steps">
        <div className="step active">1 ID Verification</div>
        <div className="step">2 Face Match</div>
        <div className="step">3 Liveness Check</div>
        <div className="step">4 KYC Result</div>
      </div>

      <h2>Upload Identity Document</h2>
      <p className="subtitle">
        Please provide a clear photo of your ID
      </p>

      {/* UPLOAD BOX */}
      <div className="upload-box">

        {!file ? (
          <>
            <div className="upload-icon">⬆</div>
            <p>Drag & drop your ID here</p>
            <span>or click to browse from your device</span>

            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFile}
              style={{ display: "none" }}
            />

            <button
              className="upload-btn"
              onClick={() => fileInputRef.current.click()}
            >
              Select Document
            </button>

            {error && <p className="error">{error}</p>}
          </>
        ) : (
          <>
            {/* FILE NAME */}
            <p className="file-name">{file.name}</p>

            {/* PREVIEW */}
            {file.type.includes("image") && (
              <img src={file.preview} className="preview-img" />
            )}

            <span>File uploaded successfully</span>
          </>
        )}
      </div>

      {/* GUIDELINES */}
      <div className="guidelines">
        <h4>Security Guidelines</h4>
        <ul>
          <li>Ensure all four corners are visible</li>
          <li>Avoid glare and shadows</li>
          <li>Text must be readable</li>
          <li>Document must be valid</li>
        </ul>
      </div>

      {/* 🔥 CONTINUE BUTTON */}
      {file && (
        <button
          className="continue-btn"
          onClick={() => navigate("/selfie")}
        >
          Continue to Face Match
        </button>
      )}

    </section>
  );
}