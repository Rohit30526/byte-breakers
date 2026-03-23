import { useNavigate } from "react-router-dom";

export default function RestartButton() {
  const navigate = useNavigate();

  return (
    <button
      className="restart-btn"
      onClick={() => navigate("/", { replace: true })}
    >
      ⟲ Restart
    </button>
  );
}