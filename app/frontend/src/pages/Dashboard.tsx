import { useState } from "react";

import GeneticRiskProfile from "../components/GeneticRiskProfile";
import ReportGenerator from "../components/ReportGenerator";
import RiskVisualization from "../components/RiskVisualization";
import ScenarioAnalysis from "../components/ScenarioAnalysis";
import ViralProfileInput from "../components/ViralProfileInput";
import { apiUrl } from "../api";
import { useRiskScore } from "../hooks/useRiskScore";
import { useSpinGlassState } from "../hooks/useSpinGlassState";
import { useVariantQuery } from "../hooks/useVariantQuery";

const defaultViral: Record<string, string | boolean> = {
  hsv1: true,
  hhv6: false,
  ebv: true,
  cmv: false,
  titer_hsv1: "medium",
  titer_hhv6: "low",
  titer_ebv: "high",
  titer_cmv: "low",
};

type Variant = { gene: string; variant: string; clinvar_pathogenicity: string };

export default function Dashboard() {
  const [viral, setViral] = useState(defaultViral);
  const [variants, setVariants] = useState<Variant[]>([]);
  const [scenarioResult, setScenarioResult] = useState<Record<string, number> | null>(null);
  const [phasePoints, setPhasePoints] = useState<Array<Record<string, string | number>>>([]);

  const { data: risk, loading, fetchRisk } = useRiskScore();
  const { state: spinState, fetchState } = useSpinGlassState();
  const { variants: searchResults, search } = useVariantQuery();

  const loadPhaseDiagram = async () => {
    const res = await fetch(apiUrl("/api/phase-diagram"));
    const body = (await res.json()) as { points: Array<Record<string, string | number>> };
    setPhasePoints(body.points);
  };

  const runRisk = async () => {
    const payload = { viral_profile: viral, variants };
    await fetchRisk(payload);
    await fetchState(viral);
  };

  const compareScenarios = async (baseline: Record<string, number>, intervention: Record<string, number>) => {
    const res = await fetch(apiUrl("/api/scenario-simulate"), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ baseline, intervention }),
    });
    setScenarioResult((await res.json()) as Record<string, number>);
  };

  return (
    <div className="grid">
      <ViralProfileInput value={viral} onChange={setViral} />
      <GeneticRiskProfile variants={variants} onChange={setVariants} searchResults={searchResults} onSearch={search} />
      <section className="card">
        <h3>Actions</h3>
        <button onClick={runRisk} disabled={loading}>{loading ? "Computing..." : "Compute MS Risk"}</button>
        <p>Coinfection state: {spinState ? `${spinState.stable_pattern}, frustration=${spinState.frustration}` : "-"}</p>
      </section>
      <RiskVisualization data={risk} />
      <section className="card">
        <h3>Phase Diagram Explorer</h3>
        <button onClick={loadPhaseDiagram}>Load phase diagram</button>
        <p>Total states: {phasePoints.length}</p>
        <p>Stable: {phasePoints.filter((p) => p.state === "stable").length}, Metastable: {phasePoints.filter((p) => p.state === "metastable").length}</p>
      </section>
      <ScenarioAnalysis onCompare={compareScenarios} />
      <section className="card">
        <h3>Scenario Comparison</h3>
        {scenarioResult ? (
          <p>Baseline: {scenarioResult.baseline_risk}, Intervention: {scenarioResult.intervention_risk}, Δ: {scenarioResult.delta}</p>
        ) : (
          <p>No comparison yet.</p>
        )}
      </section>
      <ReportGenerator risk={risk} />
      <section className="card">
        <h3>Citations & Privacy</h3>
        <details>
          <summary>Parameter notes with citations</summary>
          <p>See docs/01-viral-epidemiology.md and docs/03-coinfection-dynamics.md for viral assumptions.</p>
          <p>See docs/04-autoimmunity-mechanisms.md for host immune interpretation.</p>
        </details>
        <p>Patient inputs are anonymized in exported artifacts and are not persisted without explicit consent.</p>
      </section>
    </div>
  );
}
