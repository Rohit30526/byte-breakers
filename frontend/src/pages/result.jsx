import "../styles/result.css";
import { useNavigate } from "react-router-dom";

export default function Result() {
  const navigate = useNavigate();

  return (
    <section className="result-container">

      {/* STEPS */}
      <div className="steps">
        <div className="step done">1 ID Verification</div>
        <div className="step done">2 Face Match</div>
        <div className="step done">3 Liveness Check</div>
        <div className="step active">4 KYC Result</div>
      </div>

      {/* SUCCESS HEADER */}
      <div className="success">
        <div className="check">✔</div>
        <h2>KYC Verified Successfully</h2>
        <p>Your identity has been confirmed and your account is now active.</p>
      </div>

      {/* RESULT CARDS */}
      <div className="result-cards">

        {/* OCR DATA */}
        <div className="card">
          <h4>OCR Extraction</h4>
          <p><strong>Name:</strong> Samruddhi Rajesh Shelke</p>
          <p><strong>Aadhaar:</strong> 9576 3835 7431</p>
          <p><strong>DOB:</strong> 24/01/2007</p>
        </div>

        {/* FACE MATCH */}
        <div className="card">
          <h4>Face Match</h4>
          <h2 className="score">85%</h2>
          <p>Match Score</p>
        </div>

        {/* LIVENESS */}
        <div className="card">
          <h4>Liveness</h4>
          <p className="success-text">✅ Human Detected</p>
        </div>

      </div>

      {/* FRAUD ANALYSIS */}
      <div className="fraud-box">

        <div className="fraud-header">
          <h3>Fraud Detection Analysis</h3>
          <span className="low-risk">LOW RISK</span>
        </div>

        <div className="fraud-content">

          <div className="risk-score">
            <h1>15</h1>
            <p>Risk Score</p>
          </div>

          <div className="fraud-details">
            <p>✔ Document Authenticity Verified</p>
            <p>✔ Biometric Consistency Confirmed</p>
          </div>

        </div>

        {/* PROGRESS BAR */}
        <div className="risk-bar">
          <div className="risk-fill"></div>
        </div>

      </div>

      {/* 🔥 RESTART BUTTON */}
      <button
        className="restart-btn"
        onClick={() => navigate("/", { replace: true })}
      >
        Start New Verification
      </button>

    </section>
  );
}