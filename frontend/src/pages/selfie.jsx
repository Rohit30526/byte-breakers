import Webcam from "react-webcam";
import { useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/selfie.css";

export default function Selfie() {
  const webcamRef = useRef(null);
  const [image, setImage] = useState(null);
  const navigate = useNavigate();

  // Convert base64 → file
  const dataURLtoFile = (dataurl, filename) => {
    const arr = dataurl.split(",");
    const mime = arr[0].match(/:(.*?);/)[1];
    const bstr = atob(arr[1]);

    let n = bstr.length;
    const u8arr = new Uint8Array(n);

    while (n--) {
      u8arr[n] = bstr.charCodeAt(n);
    }

    return new File([u8arr], filename, { type: mime });
  };

  const capture = async () => {
    const screenshot = webcamRef.current.getScreenshot();
    setImage(screenshot);

    // Convert selfie
    const selfieFile = dataURLtoFile(screenshot, "selfie.jpg");

    // Get ID from previous page
    const idFile = window.selectedIdFile; // (we'll store globally)

    const formData = new FormData();
    formData.append("id_image", idFile);
    formData.append("selfie", selfieFile);

    try {
      const res = await fetch("http://127.0.0.1:8001/kyc/verify", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();

      console.log(data);

      // Navigate to result page
      navigate("/result", { state: data });

    } catch (err) {
      console.error(err);
      alert("Verification failed ❌");
    }
  };

  return (
    <section className="selfie-container">

      <div className="steps">
        <div className="step done">1. ID Verification</div>
        <div className="step active">2. Face Match</div>
        <div className="step">3. KYC Result</div>
      </div>

      <h2>Live Face Verification</h2>
      <p className="subtitle">
        Position your face and capture a selfie
      </p>

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

      {!image && (
        <button className="capture-btn" onClick={capture}>
          📸 Capture & Verify
        </button>
      )}

      <div className="tags">
        <span>Liveness</span>
        <span>Face Match</span>
        <span>Anti-Spoof</span>
      </div>

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