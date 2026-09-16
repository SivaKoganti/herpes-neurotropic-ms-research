import { useState } from "react";
import { apiUrl } from "../api";

export type RiskResponse = {
  risk_score: number;
  severity: "low" | "moderate" | "high";
  credible_interval: [number, number];
  contributions: Record<string, number>;
};

export function useRiskScore() {
  const [data, setData] = useState<RiskResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const fetchRisk = async (payload: unknown) => {
    setLoading(true);
    try {
      const res = await fetch(apiUrl("/api/risk-score"), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const body = (await res.json()) as RiskResponse;
      setData(body);
    } finally {
      setLoading(false);
    }
  };

  return { data, loading, fetchRisk };
}
