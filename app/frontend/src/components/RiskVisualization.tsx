import { PolarAngleAxis, PolarGrid, PolarRadiusAxis, Radar, RadarChart, ResponsiveContainer } from "recharts";

import { RiskResponse } from "../hooks/useRiskScore";

type Props = { data: RiskResponse | null };

export default function RiskVisualization({ data }: Props) {
  if (!data) return <section className="card"><h3>Risk Visualization</h3><p>Run a scenario to view risk.</p></section>;

  const severityColor = data.severity === "high" ? "#ef4444" : data.severity === "moderate" ? "#f59e0b" : "#10b981";
  const radar = Object.entries(data.contributions).map(([k, v]) => ({ metric: k, value: v }));

  return (
    <section className="card">
      <h3>Risk Visualization</h3>
      <p>MS Risk Score: <strong style={{ color: severityColor }}>{data.risk_score}</strong>/100</p>
      <p>Credible region: {data.credible_interval[0]} - {data.credible_interval[1]}</p>
      <div style={{ width: "100%", height: 240 }}>
        <ResponsiveContainer>
          <RadarChart data={radar}>
            <PolarGrid />
            <PolarAngleAxis dataKey="metric" />
            <PolarRadiusAxis />
            <Radar dataKey="value" stroke="#2563eb" fill="#2563eb" fillOpacity={0.4} />
          </RadarChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}
