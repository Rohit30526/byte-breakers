import { useNavigate } from "react-router-dom";
import "../styles/hero.css";
import agentImg from "../assets/bot.jpg";

export default function Hero() {
    const navigate = useNavigate();

    return (
        <section className="hero-container">

            {/* LEFT SIDE */}
            <div className="hero-left">
                <span className="badge">⚡ AI-POWERED KYC AGENT</span>

                <h1>
                    Verify <br />
                    Identity <br />
                    <span>Instantly.</span>
                </h1>

                <p>
                    RakshaKYC AI automates customer onboarding with bank-grade security,
                    facial recognition, and real-time fraud detection.
                </p>

                <div className="hero-buttons">
                    <button
                        className="primary-btn large"
                        onClick={() => navigate("/upload")}
                    >
                        Start Verification →
                    </button>
                </div>
            </div>

            {/* RIGHT SIDE */}
            <div className="hero-right">
                <div className="card-wrapper">

                    <div className="card-back"></div>

                    <div className="agent-card">
                        <div className="agent-icon">
                            <img src={agentImg} alt="AI Agent" />
                        </div>

                        <h3>Raksha AI Agent</h3>

                        <p>
                            "I'm ready to verify your identity. Please have your government ID ready."
                        </p>

                        <div className="progress-bar">
                            <div className="progress"></div>
                        </div>

                        <div className="status-row">
                            <span>SYSTEM READY</span>
                        </div>
                    </div>

                </div>
            </div>

        </section>
    );
}