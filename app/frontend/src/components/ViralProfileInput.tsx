import { ChangeEvent } from "react";

type Props = {
  value: Record<string, string | boolean>;
  onChange: (next: Record<string, string | boolean>) => void;
};

const titers = ["low", "medium", "high"];

export default function ViralProfileInput({ value, onChange }: Props) {
  const update = (key: string, val: string | boolean) => onChange({ ...value, [key]: val });

  return (
    <section className="card">
      <h3>Viral Profile Input</h3>
      {["hsv1", "hhv6", "ebv", "cmv"].map((virus) => (
        <div className="row" key={virus}>
          <label>
            <input
              type="checkbox"
              checked={Boolean(value[virus])}
              onChange={(e: ChangeEvent<HTMLInputElement>) => update(virus, e.target.checked)}
            />
            {virus.toUpperCase()}
          </label>
          <label htmlFor={`titer-${virus}`}>{virus.toUpperCase()} titer</label>
          <select
            id={`titer-${virus}`}
            value={String(value[`titer_${virus}`])}
            onChange={(e) => update(`titer_${virus}`, e.target.value)}
            title="Titer levels represent relative serologic signal intensity."
          >
            {titers.map((t) => (
              <option key={t} value={t}>{t}</option>
            ))}
          </select>
        </div>
      ))}
    </section>
  );
}
