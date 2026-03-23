import Webcam from "react-webcam";
import { useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/selfie.css";

export default function Selfie() {
  const webcamRef = useRef(null);
  const [image, setImage] = useState(null);
  const navigate = useNavigate();

  const capture = () => {
    const screenshot = webcamRef.current.getScreenshot();
    setImage(screenshot);

    // simulate processing → next page
    setTimeout(() => {
      navigate("/result");
    }, 1500);
  };

  return (
    <section className="selfie-container">

      {/* STEPS */}
      <div className="steps">
        <div className="step done">1. ID Verification</div>
        <div className="step active">2. Face Match</div>
        <div className="step">3. KYC Result</div>
      </div>

      <h2>Live Face Verification</h2>
      <p className="subtitle">
        Position your face and capture a selfie
      </p>

      {/* CAMERA */}
      <div className="camera-box">
        {!image ? (
          <Webcam
            ref={webcamRef}
            screenshotFormat="image/jpeg"
            className="webcam"
          />
        ) : (
          <img src={image} alt="selfie" className="webcam" />
        )}
      </div>

      {/* BUTTON */}
      {!image && (
        <button className="capture-btn" onClick={capture}>
          📸 Capture Selfie
        </button>
      )}

      {/* TAGS */}
      <div className="tags">
        <span>Liveness</span>
        <span>Face Match</span>
        <span>Anti-Spoof</span>
      </div>

      {/* GUIDELINES */}
      <div className="guidelines">
        <h4>Capture Tips</h4>
        <ul>
          <li>Ensure good lighting</li>
          <li>Remove glasses or mask</li>
          <li>Keep neutral expression</li>
          <li>Stay still</li>
        </ul>
      </div>

    </section>
  );
}