import "../styles/result.css";
import { useNavigate, useLocation } from "react-router-dom";

export default function Result() {
  const navigate = useNavigate();
  const { state } = useLocation();

  if (!state) return <h2>No Data</h2>;

  const { ocr, face_match, liveness, risk_score, status } = state;

  return (
    <section className="result-container">

      <div className="steps">
        <div className="step done">1 ID Verification</div>
        <div className="step done">2 Face Match</div>
        <div className="step done">3 Liveness Check</div>
        <div className="step active">4 KYC Result</div>
      </div>

      {/* HEADER */}
      <div className="success">
        <div className="check">✔</div>
        <h2>{status === "Verified" ? "KYC Verified Successfully" : "KYC Failed"}</h2>
        <p>Your identity verification result is shown below.</p>
      </div>

      {/* CARDS */}
      <div className="result-cards">

        {/* OCR */}
       <div className="card">
  <h4>OCR Extraction</h4>

  <p>
    <strong>Name:</strong>{" "}
    {state?.ocr?.data?.name || "Not Found"}
  </p>

  <p>
    <strong>Aadhaar:</strong>{" "}
    {state?.ocr?.data?.aadhaar || "Not Found"}
  </p>

  <p>
    <strong>DOB:</strong>{" "}
    {state?.ocr?.data?.dob || "Not Found"}
  </p>
</div>

        {/* FACE */}
        <div className="card">
  <h4>Face Match</h4>

  <h2 className="score">
    {state.face_match.confidence.toFixed(0)}%
  </h2>

  <p>
    {state.face_match.match
      ? "✅ Match Successful"
      : "❌ Face Mismatch"}
  </p>
</div>

        {/* LIVENESS */}
        <div className="card">
          <h4>Liveness</h4>
          <p className="success-text">
            {liveness ? "✅ Human Detected" : "❌ Spoof Detected"}
          </p>
        </div>

      </div>

      {/* FRAUD */}
      <div className="fraud-box">

        <div className="fraud-header">
          <h3>Fraud Detection Analysis</h3>
          <span className={risk_score < 30 ? "low-risk" : "high-risk"}>
            {risk_score < 30 ? "LOW RISK" : "HIGH RISK"}
          </span>
        </div>

        <div className="fraud-content">
          <div className="risk-score">
            <h1>{risk_score}</h1>
            <p>Risk Score</p>
          </div>

          <div className="fraud-details">
            <p>✔ Face Match: {face_match.match ? "Yes" : "No"}</p>
            <p>✔ Liveness: {liveness ? "Valid" : "Invalid"}</p>
          </div>
        </div>

        <div className="risk-bar">
          <div
            className="risk-fill"
            style={{ width: `${risk_score}%` }}
          ></div>
        </div>

      </div>

      <button
        className="restart-btn"
        onClick={() => navigate("/", { replace: true })}
      >
        Start New Verification
      </button>

    </section>
  );
}