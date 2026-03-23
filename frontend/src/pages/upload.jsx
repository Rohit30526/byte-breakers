import "../styles/upload.css";

export default function Upload() {
  return (
    <div className="upload-page">

      {/* Title */}
      <h1 className="title">Upload Identity Document</h1>
      <p className="subtitle">
        Please provide a clear photo of your government-issued ID 
        (Passport, Driver's License, or National ID).
      </p>

      {/* Upload Box */}
      <div className="upload-box">

        <div className="upload-icon">⬆️</div>

        <p className="drag-text">Drag and drop your ID here</p>
        <p className="browse-text">
          or click to browse from your device
        </p>

        <button className="upload-btn">Select Document</button>

        <div className="features">
          <div>📄 OCR READY</div>
          <div>✔ AUTHENTIC</div>
          <div>🖼 HIGH RES</div>
        </div>
      </div>

      {/* Guidelines */}
      <div className="guidelines">
        <h3>SECURITY GUIDELINES</h3>
        <ul>
          <li>Ensure all four corners of the ID are visible</li>
          <li>Avoid glare and shadows on the document</li>
          <li>The text must be clearly readable</li>
          <li>Document must be valid and not expired</li>
        </ul>
      </div>

    </div>
  );
}