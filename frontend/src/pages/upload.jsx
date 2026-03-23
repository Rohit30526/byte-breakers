import "../styles/upload.css";

export default function Upload() {
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

        <button className="upload-btn">Select Document</button>

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