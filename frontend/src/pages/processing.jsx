import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function Processing() {
  const navigate = useNavigate();

  useEffect(() => {
    setTimeout(() => {
      navigate("/result");
    }, 2000);
  }, []);

  return (
    <div style={{ textAlign: "center", padding: "100px" }}>
      <h2>🔍 Verifying your document...</h2>
    </div>
  );
}