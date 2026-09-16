import { useState } from "react";

type Variant = { gene: string; variant: string; clinvar_pathogenicity: string };

type Props = {
  variants: Variant[];
  onChange: (variants: Variant[]) => void;
  searchResults: Array<Record<string, string | number>>;
  onSearch: (gene?: string) => void;
};

export default function GeneticRiskProfile({ variants, onChange, searchResults, onSearch }: Props) {
  const [gene, setGene] = useState("TLR2");

  return (
    <section className="card">
      <h3>Genetic Risk Profile</h3>
      <div className="row">
        <input value={gene} onChange={(e) => setGene(e.target.value)} placeholder="Gene (e.g., TLR2)" />
        <button onClick={() => onSearch(gene)}>Search ClinVar</button>
      </div>
      <ul>
        {searchResults.map((r) => (
          <li key={`${String(r.gene)}-${String(r.variant)}`}>
            {r.gene} {r.variant} ({r.pathogenicity})
            <button
              onClick={() =>
                onChange([
                  ...variants,
                  {
                    gene: String(r.gene),
                    variant: String(r.variant),
                    clinvar_pathogenicity: String(r.pathogenicity),
                  },
                ])
              }
            >
              Add
            </button>
          </li>
        ))}
      </ul>
      <p>Risk allele count: {variants.length}</p>
    </section>
  );
}
