import { useState } from "react";

type Scenario = { reactivation_rate: number; cns_tropism: number; immune_suppression: number; antiviral_therapy: number };

type Props = {
  onCompare: (baseline: Scenario, intervention: Scenario) => Promise<void>;
};

export default function ScenarioAnalysis({ onCompare }: Props) {
  const [baseline, setBaseline] = useState<Scenario>({ reactivation_rate: 0.6, cns_tropism: 0.5, immune_suppression: 0.4, antiviral_therapy: 0.1 });
  const [intervention, setIntervention] = useState<Scenario>({ reactivation_rate: 0.5, cns_tropism: 0.4, immune_suppression: 0.3, antiviral_therapy: 0.6 });
  const labels: Record<keyof Scenario, string> = {
    reactivation_rate: "Reactivation rate",
    cns_tropism: "CNS tropism",
    immune_suppression: "Immune suppression",
    antiviral_therapy: "Antiviral therapy",
  };

  const renderSlider = (
    section: "baseline" | "intervention",
    label: keyof Scenario,
    source: Scenario,
    setter: (s: Scenario) => void
  ) => {
    const inputId = `${section}-${label}`;
    return (
      <div className="row">
        <label htmlFor={inputId}>{labels[label]}</label>
        <input
          id={inputId}
        type="range"
        min={0}
        max={1}
        step={0.05}
        value={source[label]}
          aria-valuetext={`${source[label]}`}
        onChange={(e) => setter({ ...source, [label]: Number(e.target.value) })}
      />
        <output>{source[label]}</output>
      </div>
    );
  };

  return (
    <section className="card">
      <h3>Scenario Analysis</h3>
      <h4>Baseline</h4>
      {renderSlider("baseline", "reactivation_rate", baseline, setBaseline)}
      {renderSlider("baseline", "cns_tropism", baseline, setBaseline)}
      {renderSlider("baseline", "immune_suppression", baseline, setBaseline)}
      {renderSlider("baseline", "antiviral_therapy", baseline, setBaseline)}
      <h4>Intervention</h4>
      {renderSlider("intervention", "reactivation_rate", intervention, setIntervention)}
      {renderSlider("intervention", "cns_tropism", intervention, setIntervention)}
      {renderSlider("intervention", "immune_suppression", intervention, setIntervention)}
      {renderSlider("intervention", "antiviral_therapy", intervention, setIntervention)}
      <button onClick={() => onCompare(baseline, intervention)}>Compare scenarios</button>
    </section>
  );
}
