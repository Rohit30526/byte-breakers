import { Routes, Route } from "react-router-dom";
import MainLayout from "./layout/mainlayout";
import Hero from "./pages/hero";
import Upload from "./pages/upload";
import Selfie from "./pages/selfie";

function App() {
  return (
    <MainLayout>
      <Routes>
        <Route path="/" element={<Hero />} />
        <Route path="/upload" element={<Upload />} />
        <Route path="/selfie" element={<Selfie />} />
      </Routes>
    </MainLayout>
  );
}

export default App;