import Webcam from "react-webcam";
import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/liveness.css";

export default function Liveness() {
  const webcamRef = useRef(null);
  const navigate = useNavigate();

  const steps = [
    "Look straight",
    "Turn your head left",
    "Turn your head right",
    "Blink your eyes"
  ];

  const [currentStep, setCurrentStep] = useState(0);

  // 🔥 simulate liveness steps
  useEffect(() => {
    if (currentStep < steps.length) {
      const timer = setTimeout(() => {
        setCurrentStep((prev) => prev + 1);
      }, 2000);

      return () => clearTimeout(timer);
    } else {
      // done → go to result
      setTimeout(() => {
        navigate("/result");
      }, 1000);
    }
  }, [currentStep]);

  return (
    <section className="liveness-container">

      {/* STEPS HEADER */}
      <div className="steps">
        <div className="step done">1 ID</div>
        <div className="step done">2 Face</div>
        <div className="step active">3 Liveness</div>
        <div className="step">4 Result</div>
      </div>

      <h2>Liveness Detection</h2>
      <p className="subtitle">
        Follow the instructions to verify you're a real person
      </p>

      {/* CAMERA */}
      <div className="camera-box">
        <Webcam ref={webcamRef} className="webcam" />

        {/* INSTRUCTION BOX */}
        {currentStep < steps.length && (
          <div className="instruction-box">
            <p className="label">CURRENT ACTION</p>
            <h3>{steps[currentStep]}</h3>
          </div>
        )}
      </div>

      {/* STEP INDICATORS */}
      <div className="liveness-steps">
        {steps.map((step, index) => (
          <div
            key={index}
            className={`circle ${
              index < currentStep ? "done" : index === currentStep ? "active" : ""
            }`}
          />
        ))}
      </div>

    </section>
  );
}