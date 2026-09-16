import { useState } from "react";

type Scenario = { reactivation_rate: number; cns_tropism: number; immune_suppression: number; antiviral_therapy: number };

type Props = {
  onCompare: (baseline: Scenario, intervention: Scenario) => Promise<void>;
};

export default function ScenarioAnalysis({ onCompare }: Props) {
  const [baseline, setBaseline] = useState<Scenario>({ reactivation_rate: 0.6, cns_tropism: 0.5, immune_suppression: 0.4, antiviral_therapy: 0.1 });
  const [intervention, setIntervention] = useState<Scenario>({ reactivation_rate: 0.5, cns_tropism: 0.4, immune_suppression: 0.3, antiviral_therapy: 0.6 });

  const renderSlider = (label: keyof Scenario, source: Scenario, setter: (s: Scenario) => void) => (
    <label className="row">
      {label}
      <input
        type="range"
        min={0}
        max={1}
        step={0.05}
        value={source[label]}
        onChange={(e) => setter({ ...source, [label]: Number(e.target.value) })}
      />
      {source[label]}
    </label>
  );

  return (
    <section className="card">
      <h3>Scenario Analysis</h3>
      <h4>Baseline</h4>
      {renderSlider("reactivation_rate", baseline, setBaseline)}
      {renderSlider("cns_tropism", baseline, setBaseline)}
      {renderSlider("immune_suppression", baseline, setBaseline)}
      {renderSlider("antiviral_therapy", baseline, setBaseline)}
      <h4>Intervention</h4>
      {renderSlider("reactivation_rate", intervention, setIntervention)}
      {renderSlider("cns_tropism", intervention, setIntervention)}
      {renderSlider("immune_suppression", intervention, setIntervention)}
      {renderSlider("antiviral_therapy", intervention, setIntervention)}
      <button onClick={() => onCompare(baseline, intervention)}>Compare scenarios</button>
    </section>
  );
}
