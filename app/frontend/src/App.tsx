import { useState } from "react";

import About from "./pages/About";
import Dashboard from "./pages/Dashboard";
import Documentation from "./pages/Documentation";

type Page = "dashboard" | "docs" | "about";

export default function App() {
  const [page, setPage] = useState<Page>("dashboard");
  const [dark, setDark] = useState(true);

  return (
    <main className="app" style={{ background: dark ? "#111" : "#fafafa", color: dark ? "#f5f5f5" : "#111" }}>
      <div className="row">
        <button onClick={() => setPage("dashboard")}>Dashboard</button>
        <button onClick={() => setPage("docs")}>Documentation</button>
        <button onClick={() => setPage("about")}>About</button>
        <button onClick={() => setDark((v) => !v)}>{dark ? "Light mode" : "Dark mode"}</button>
      </div>
      {page === "dashboard" && <Dashboard />}
      {page === "docs" && <Documentation />}
      {page === "about" && <About />}
    </main>
  );
}
