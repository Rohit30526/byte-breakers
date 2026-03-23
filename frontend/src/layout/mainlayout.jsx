import logo from "../assets/bot.jpg";
import RestartButton from "../components/RestartButton";

export default function MainLayout({ children }) {
  return (
    <div style={{ padding: "20px 60px" }}>
      
      {/* NAVBAR */}
      <nav
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "40px",
        }}
      >
        {/* LOGO */}
        <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
          <img src={logo} alt="logo" style={{ height: "32px" }} />
          <span style={{ fontWeight: "600" }}>RakshaKYC AI</span>
        </div>

        {/* ✅ GLOBAL RESTART BUTTON */}
        <RestartButton />
      </nav>

      {/* PAGE CONTENT */}
      {children}
    </div>
  );
}