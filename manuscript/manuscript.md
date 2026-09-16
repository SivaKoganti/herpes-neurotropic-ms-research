# Working manuscript draft for repository-based preprint assembly

> **Placeholder requiring author/journal decision:** final title, author list, affiliations, corresponding author, target journal or preprint server, abstract word count, and reference style.
>
> **Current status:** this draft is prepared for manuscript drafting and preprint preparation from the integrated repository state. It is **not** a claim of final journal-submission readiness.

## Title

**Working title:** Integrated literature synthesis, exploratory coinfection simulation, and ClinVar-linked host susceptibility reporting for herpes/neurotropic virus hypotheses in multiple sclerosis

## Abstract

This repository-centered manuscript draft describes an integrated research resource focused on hypotheses linking herpes and other neurotropic viruses to multiple sclerosis (MS). The repository combines (i) narrative literature-synthesis chapters in `docs/`, (ii) a simulated spin-glass coinfection model in `analysis/spin_glass_coinfection_model.py`, (iii) an exploratory ClinVar-derived host susceptibility workflow in `analysis/clinvar_viral_susceptibility_analysis.py`, and (iv) a FastAPI/React decision-support application under `app/`. The present draft reports only repository-supported artifacts and workflow outputs. It does not claim experimental validation, patient-level clinical performance, or causal inference. Generated artifacts currently include two spin-glass CSV outputs, three ClinVar-derived CSV summaries, one GraphML association network, and runtime application exports. These materials can support preprint assembly if authors complete citation verification, venue-specific formatting, and expert review of scientific claims. All modeled outputs should remain framed as exploratory research or decision-support artifacts rather than diagnostic conclusions.

## Introduction

The repository addresses a broad and unresolved hypothesis space at the intersection of viral neurotropism, immune dysregulation, and MS pathogenesis. The literature-review chapters collect candidate mechanisms such as viral persistence, reactivation, molecular mimicry, and blood-brain barrier disruption. The computational layer then provides two exploratory complements to the narrative review:

1. a spin-glass-inspired simulation of competing viral states across central nervous system compartments, and
2. a ClinVar-derived workflow that ranks example host genetic features associated with viral persistence or reactivation fields in the repository dataset.

The integrated application exposes these exploratory models in a browser-accessible interface, but the repository explicitly states that application outputs are not clinical diagnosis. Accordingly, this manuscript draft is written as a computational/review methods paper rather than a clinical or translational validation study.

## Research Questions

1. How can the repository's literature-synthesis chapters be organized into a manuscript-ready narrative about neurotropic viral hypotheses in MS?
2. What exactly do the simulated spin-glass outputs contribute, and what do they *not* establish?
3. How should the ClinVar-derived exploratory associations be described without overstating evidentiary strength?
4. How can the decision-support application be documented as a reproducible research interface while preserving its non-diagnostic framing?
5. What publication blockers remain before preprint posting or eventual journal submission?

## Methods

### Study design and repository scope

This manuscript draft describes the integrated repository state represented by the README, literature chapters, analysis scripts, generated `figures/` artifacts, and application documentation. The work is a mixed-format repository synthesis rather than a prospective human-subject experiment.

### Data sources

#### Literature synthesis inputs

- `docs/01-viral-epidemiology.md`
- `docs/02-viral-pathogenesis.md`
- `docs/03-coinfection-dynamics.md`
- `docs/04-autoimmunity-mechanisms.md`
- `docs/05-ms-pathogenesis-links.md`
- `REFERENCES.md`

These files provide topic scaffolding and draft mechanistic claims. Because `REFERENCES.md` remains partly a structured bibliography framework, any manuscript claim tied to the literature must be checked against exact source citations before external submission.

#### Structured computational inputs

- `data/clinvar-ms-variants.csv`: repository-tracked example dataset used by the ClinVar analysis workflow.
- Implicit spin-glass parameter grids defined in `analysis/spin_glass_coinfection_model.py`.

### Computational analyses

#### Spin-glass coinfection workflow

`analysis/spin_glass_coinfection_model.py` defines a discrete-state coinfection simulation with four viruses (`HSV1`, `HHV6`, `EBV`, `CMV`), three compartments (`grey_matter`, `white_matter_lesion`, `csf`), fixed random seeds, and a Metropolis-style sampling procedure. It generates:

- `figures/spin_glass_phase_diagram.csv`
- `figures/spin_glass_frustration_landscape.csv`

These outputs are simulations of model behavior over temperature and viral-burden-shift grids. They are not direct measurements from patients, tissues, or animal models.

#### ClinVar-derived exploratory workflow

`analysis/clinvar_viral_susceptibility_analysis.py` reads `data/clinvar-ms-variants.csv`, annotates pathway groups, calculates pathway enrichment summaries, estimates exploratory logistic reactivation scores, runs a permutation-based association test, and writes:

- `figures/clinvar_pathway_enrichment.csv`
- `figures/host_genetic_predisposition_scores.csv`
- `figures/clinvar_association_summary.csv`
- `figures/host_genetic_viral_network.graphml`

These outputs summarize the repository's curated example dataset and should be described as exploratory or hypothesis-generating only.

#### Decision-support application

The repository includes a FastAPI backend and React frontend under `app/`. The application consumes viral profile inputs and variant entries, exposes `/api` routes for scoring and reporting, and can export runtime PDF/JSON/CSV outputs. The repository documentation and tests explicitly preserve a non-diagnostic disclaimer for these reports.

## Results and reporting of generated artifacts

### Literature synthesis status

The current literature narrative is distributed across five thematic documents covering epidemiology, pathogenesis, coinfection dynamics, autoimmunity mechanisms, and MS pathogenesis links. These chapters are suitable as drafting inputs but still require source-level citation completion and editorial harmonization before submission.

### Spin-glass outputs

- `figures/spin_glass_phase_diagram.csv` contains 56 simulated parameter combinations across temperature and burden-shift settings.
- `figures/spin_glass_frustration_landscape.csv` contains the corresponding 56-row frustration-oriented summary.
- Reported columns include mean replication, mean latency, frustration index, replica order parameter, final energy, and reactivation cascade risk.

These are generated computational outputs. They should be interpreted as model-behavior summaries that illustrate how the repository encodes competing coinfection states, not as empirical evidence that a corresponding biological phase diagram has been observed in MS.

### ClinVar-derived exploratory outputs

- `figures/clinvar_pathway_enrichment.csv` summarizes 5 pathway-level enrichment rows from the repository dataset.
- `figures/host_genetic_predisposition_scores.csv` ranks 16 example variant records with a `score_mode` column documenting whether the workflow used cross-validated or fallback scoring.
- `figures/clinvar_association_summary.csv` records `n_variants = 16`, `n_pathogenic = 13`, and an exploratory permutation p-value of `0.033932135728542916` under the default script settings.
- `figures/host_genetic_viral_network.graphml` stores a 24-node, 31-edge network linking pathway, gene, and outcome nodes.

These outputs summarize the repository's example ClinVar-derived dataset only. They do not demonstrate clinical sensitivity/specificity, prospective risk prediction, or causal host-virus mechanisms.

### Decision-support application outputs

The application can generate runtime PDF/JSON/CSV summaries from user-provided viral and variant inputs. The repository presently supports this as an exploratory interface for inspecting modeled outputs and communicating reproducible examples. The application should not be presented as a validated clinical decision system, and any screenshots or exports used in a preprint should retain the repository's non-diagnostic framing.

## Discussion

The integrated repository is strongest as a hypothesis-organizing and workflow-demonstration resource. Its value lies in aligning a narrative review with reproducible scripts, tracked example outputs, and an application layer that exposes the same concepts interactively. This allows authors to show how literature-derived questions map onto explicit computational artifacts.

At the same time, the integrated structure increases the risk of overstatement if manuscript text blurs the boundaries between evidence types. The review chapters synthesize concepts from the literature, the spin-glass module generates simulated states, the ClinVar workflow produces exploratory associations from a repository-tracked example dataset, and the application packages those outputs into a reusable interface. These components can coexist in one paper, but only if the manuscript repeatedly distinguishes literature synthesis from simulation, exploratory computational scoring, and non-diagnostic software reporting.

## Limitations

1. The repository does not yet contain a fully verified manuscript bibliography with exact article citations for every biomedical claim.
2. The spin-glass outputs are simulation-derived and do not constitute biological validation.
3. The ClinVar workflow operates on a small, repository-curated example dataset and should not be interpreted as a clinical or epidemiologic cohort analysis.
4. The application scoring logic is exploratory and not calibrated for diagnostic use, treatment selection, or patient management.
5. Author metadata, venue formatting, conflict-of-interest statements, and submission-specific compliance items remain unresolved placeholders.

## Reproducibility

The repository documents a root-level reproducibility workflow:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=app/backend python -m pytest -q
python analysis/spin_glass_coinfection_model.py
python analysis/clinvar_viral_susceptibility_analysis.py
cd app/frontend && npm ci && npm run build && cd ../..
```

The deterministic analysis outputs in `figures/` should regenerate without diffs when the fixed seeds and current inputs are unchanged. Before preprint assembly, authors should rerun the workflow, confirm that manuscript tables and legends still match the tracked artifact files, and update any claim-traceability rows affected by edits.

## Ethics and safety framing

- This repository does not provide clinical diagnosis.
- Application outputs are research/decision-support artifacts only.
- Any use of patient identifiers in runtime exports should remain anonymized unless separately approved and governed.
- No patient-level validation, interventional study, or bedside deployment claim should be made from the current repository state.
- Manuscript text should avoid unsupported causal statements linking any specific virus, coinfection pattern, or host genotype to MS onset or progression.

## Figure legends

**Figure 1. Simulated spin-glass phase diagram for coinfection state summaries.** Derived from `figures/spin_glass_phase_diagram.csv`, generated by `analysis/spin_glass_coinfection_model.py` across temperature and burden-shift grids. Recommended display: a heatmap or faceted scatter summarizing mean replication or reactivation-cascade risk. Interpretation should remain limited to simulated model behavior.

**Figure 2. Simulated frustration landscape across the same parameter grid.** Derived from `figures/spin_glass_frustration_landscape.csv`. Recommended display: a heatmap or contour plot of frustration index, replica order parameter, or final energy. This figure illustrates internal disorder metrics within the simulation rather than observed CNS measurements.

**Figure 3. Exploratory pathway-level summary of repository-tracked ClinVar records.** Derived from `figures/clinvar_pathway_enrichment.csv`, generated by `analysis/clinvar_viral_susceptibility_analysis.py`. Recommended display: a bar chart or dot plot of pathway-level persistence enrichment and pathway fractions. Any caption should state that the inputs are repository-curated example records rather than a validated patient cohort.

**Figure 4. Ranked host genetic predisposition scores from the repository example dataset.** Derived from `figures/host_genetic_predisposition_scores.csv`. Recommended display: a ranked bar chart or lollipop plot of `host_genetic_predisposition_score` with `score_mode` annotation. This figure is exploratory and not a clinically validated risk ranking.

**Figure 5. Host-pathway-outcome association network.** Derived from `figures/host_genetic_viral_network.graphml`. Recommended display: a force-directed network diagram distinguishing outcome, pathway, and gene nodes. Edge weights reflect within-repository summary statistics, not experimentally measured mechanistic strengths.

**Table 1. Repository artifact inventory for manuscript assembly.** Inventory of tracked outputs, source scripts, inputs, interpretations, and limitations.

**Table 2. Claim traceability table.** Crosswalk between manuscript claims, repository evidence, and literature placeholders that still require exact citation verification.

## Figure and table inventory

| Manuscript item | Artifact path | Source script or component | Upstream input(s) | Intended interpretation | Key limitation(s) |
| --- | --- | --- | --- | --- | --- |
| Figure 1 | `figures/spin_glass_phase_diagram.csv` | `analysis/spin_glass_coinfection_model.py` | Internal parameter grid over temperature and burden shift | Simulated summary of modeled coinfection states | Simulation only; not patient or experimental data |
| Figure 2 | `figures/spin_glass_frustration_landscape.csv` | `analysis/spin_glass_coinfection_model.py` | Internal parameter grid over temperature and burden shift | Simulated disorder/frustration metrics and derived cascade risk | Model-derived quantities depend on encoded assumptions |
| Figure 3 | `figures/clinvar_pathway_enrichment.csv` | `analysis/clinvar_viral_susceptibility_analysis.py` | `data/clinvar-ms-variants.csv` | Exploratory pathway-level persistence/reactivation summary | Example repository dataset; not a cohort-wide enrichment study |
| Figure 4 | `figures/host_genetic_predisposition_scores.csv` | `analysis/clinvar_viral_susceptibility_analysis.py` | `data/clinvar-ms-variants.csv` | Exploratory ranking of repository variant records | Score is not clinically validated or calibrated |
| Figure 5 | `figures/host_genetic_viral_network.graphml` | `analysis/clinvar_viral_susceptibility_analysis.py` | `data/clinvar-ms-variants.csv` | Network view of pathway, gene, and outcome links | Edge weights are summary statistics from the repository dataset |
| Table-ready summary | `figures/clinvar_association_summary.csv` | `analysis/clinvar_viral_susceptibility_analysis.py` | `data/clinvar-ms-variants.csv` | Compact record of dataset size and permutation output | Exploratory association only; requires careful narrative framing |
| Workflow illustration | `app/backend/app/services/report_generator.py` runtime PDF/JSON/CSV exports | FastAPI backend + React frontend under `app/` | User-supplied viral profile and variant payloads | Example research-reporting interface for repository outputs | Runtime artifacts are non-diagnostic and not versioned in `figures/` |

## Claim traceability

| Claim ID | Manuscript claim | Evidence or reference key | Status / action before submission |
| --- | --- | --- | --- |
| C1 | The repository integrates literature-synthesis chapters, exploratory analysis scripts, generated artifacts, and a decision-support application. | `README.md`; `app/README.md` | Repository-verified |
| C2 | The spin-glass workflow simulates four viruses across grey matter, white matter lesion, and CSF compartments using fixed-seed sampling. | `analysis/spin_glass_coinfection_model.py` | Repository-verified |
| C3 | The spin-glass script writes two tracked CSV outputs for phase and frustration summaries. | `analysis/spin_glass_coinfection_model.py`; `figures/spin_glass_phase_diagram.csv`; `figures/spin_glass_frustration_landscape.csv` | Repository-verified |
| C4 | The repository-tracked ClinVar workflow currently summarizes 16 example records, including 13 pathogenic or likely pathogenic classifications in the generated summary. | `data/clinvar-ms-variants.csv`; `figures/clinvar_association_summary.csv` | Repository-verified |
| C5 | The default ClinVar script settings produce an exploratory permutation p-value of `0.033932135728542916` in the tracked summary file. | `figures/clinvar_association_summary.csv`; `tests/test_analysis_modules.py` | Repository-verified; keep labeled exploratory |
| C6 | The application and exported reports are explicitly framed as research/decision-support outputs rather than clinical diagnosis. | `README.md`; `app/README.md`; `app/backend/tests/test_api.py` | Repository-verified |
| C7 | EBV seropositivity correlates with MS incidence. | `REF-EBV-MS` in `REFERENCES.md` | Requires exact source citation verification |
| C8 | HHV-6 has been reported at higher frequency in MS-associated CNS/CSF contexts than in controls. | `REF-HHV6-MS` in `REFERENCES.md` | Requires exact source citation verification |
| C9 | Molecular mimicry between viral antigens and myelin-associated targets has been proposed as one mechanism relevant to MS hypotheses. | `REF-MIMICRY` in `REFERENCES.md` | Requires exact source citation verification |
| C10 | Viral reactivation has been discussed as a possible temporal correlate of MS relapses. | `REF-RELAPSE` in `REFERENCES.md` | Requires exact source citation verification |
| C11 | Viral effects on blood-brain barrier integrity are part of the repository's mechanistic framing. | `REF-BBB` in `REFERENCES.md` | Requires exact source citation verification |

## References

### Repository artifacts cited directly in this draft

- `README.md`
- `REFERENCES.md`
- `docs/01-viral-epidemiology.md`
- `docs/02-viral-pathogenesis.md`
- `docs/03-coinfection-dynamics.md`
- `docs/04-autoimmunity-mechanisms.md`
- `docs/05-ms-pathogenesis-links.md`
- `analysis/spin_glass_coinfection_model.py`
- `analysis/clinvar_viral_susceptibility_analysis.py`
- `data/clinvar-ms-variants.csv`
- `figures/spin_glass_phase_diagram.csv`
- `figures/spin_glass_frustration_landscape.csv`
- `figures/clinvar_pathway_enrichment.csv`
- `figures/host_genetic_predisposition_scores.csv`
- `figures/clinvar_association_summary.csv`
- `figures/host_genetic_viral_network.graphml`
- `app/README.md`
- `app/backend/tests/test_api.py`
- `tests/test_analysis_modules.py`

### Literature references still requiring exact citation completion

- `REF-EBV-MS`
- `REF-HSV-MS`
- `REF-HHV6-MS`
- `REF-MIMICRY`
- `REF-BBB`
- `REF-RELAPSE`
