import logo from "../assets/bot.jpg";

export default function MainLayout({ children }) {
  return (
    <div style={{ padding: "20px 60px" }}>
      {/* Navbar */}
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

        {/* Restart Button */}
        <button
          style={{
            background: "#0f172a",
            color: "white",
            border: "none",
            padding: "8px 18px",
            borderRadius: "10px",
            cursor: "pointer",
          }}
        >
          Restart
        </button>
      </nav>

      {children}
    </div>
  );
}