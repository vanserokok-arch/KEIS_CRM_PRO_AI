import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import "../styles/index.css";
import { api } from "../shared/api/http";

function Home() {
  const [status, setStatus] = React.useState<string>("…");

  React.useEffect(() => {
    api.get("/health").then(r => setStatus(r.data.status)).catch(() => setStatus("error"));
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>KEIS CRM PRO AI — Frontend работает!</h1>
      <p>Если ты видишь это, React + Vite настроены верно.</p>
      <p>Бэкенд: <b>{status}</b></p>
      <nav style={{ marginTop: 16 }}>
        <Link to="/kanban" style={{ marginRight: 12 }}>Kanban</Link>
        <Link to="/list">List</Link>
      </nav>
    </div>
  );
}

function Kanban()   { return <div style={{ padding: 20 }}>Kanban view (заглушка)</div>; }
function ListView() { return <div style={{ padding: 20 }}>List view (заглушка)</div>; }

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/kanban" element={<Kanban />} />
        <Route path="/list" element={<ListView />} />
      </Routes>
    </BrowserRouter>
  );
}

ReactDOM.createRoot(document.getElementById("root")!).render(<App />);