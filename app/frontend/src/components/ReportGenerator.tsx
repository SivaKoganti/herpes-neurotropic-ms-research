import { RiskResponse } from "../hooks/useRiskScore";
import { apiUrl } from "../api";

type Props = { risk: RiskResponse | null };

export default function ReportGenerator({ risk }: Props) {
  const csvEscape = (value: string | number) => `"${String(value).replace(/"/g, '""')}"`;

  const generate = async () => {
    if (!risk) return;
    const resp = await fetch(apiUrl("/api/generate-report"), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ patient_id: "ANON", risk_result: risk, notes: "Generated from dashboard" }),
    });
    const blob = await resp.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "ms-risk-report.pdf";
    a.click();
    window.URL.revokeObjectURL(url);
  };

  return (
    <section className="card">
      <h3>Report Generator</h3>
      <button onClick={generate} disabled={!risk}>Download PDF Report</button>
      <button
        onClick={() => {
          if (!risk) return;
          const data = `data:text/json;charset=utf-8,${encodeURIComponent(JSON.stringify(risk, null, 2))}`;
          const a = document.createElement("a");
          a.href = data;
          a.download = "ms-risk.json";
          a.click();
        }}
        disabled={!risk}
      >
        Export JSON
      </button>
      <button
        onClick={() => {
          if (!risk) return;
          const rows = Object.entries(risk.contributions)
            .map(([k, v]) => `${csvEscape(k)},${csvEscape(v)}`)
            .join("\n");
          const csv = `metric,value\n${csvEscape("risk_score")},${csvEscape(risk.risk_score)}\n${csvEscape("severity")},${csvEscape(risk.severity)}\n${rows}`;
          const data = `data:text/csv;charset=utf-8,${encodeURIComponent(csv)}`;
          const a = document.createElement("a");
          a.href = data;
          a.download = "ms-risk.csv";
          a.click();
        }}
        disabled={!risk}
      >
        Export CSV
      </button>
    </section>
  );
}
