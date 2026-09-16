# Herpes Virus & Neurotropic Virus Coinfection in Multiple Sclerosis: Deep Review

## Overview

This repository contains a comprehensive deep review examining the potential roles of herpes simplex virus (HSV), human herpesvirus-6 (HHV-6), and other neurotropic viruses in multiple sclerosis (MS) pathogenesis, with particular focus on viral coinfection scenarios.

## Key Research Questions

- What is the epidemiological evidence linking herpes viruses to MS risk?
- How do neurotropic viruses establish persistent CNS infections?
- What mechanisms could drive viral coinfection-mediated autoimmunity?
- Can viral reactivation trigger MS exacerbations?
- What therapeutic implications emerge from viral-autoimmune models?

## Repository Structure

```
├── README.md                           # This file
├── manuscript/
│   └── manuscript.md                   # Draft IMRaD-style manuscript for preprint assembly
├── app/
│   ├── README.md                       # Interactive web app setup
│   ├── frontend/                       # React dashboard
│   └── backend/                        # FastAPI risk API
├── docs/
│   ├── 01-viral-epidemiology.md       # Epidemiological evidence
│   ├── 02-viral-pathogenesis.md       # Mechanisms of neurotropism
│   ├── 03-coinfection-dynamics.md     # Viral interactions & synergy
│   ├── 04-autoimmunity-mechanisms.md  # Molecular mimicry, bystander activation
│   └── 05-ms-pathogenesis-links.md    # Connection to MS pathology
├── data/
│   ├── clinvar-ms-variants.csv        # Filtered ClinVar MS + immune variants
│   └── (additional literature/data inputs may be added as curated assets)
├── analysis/
│   ├── spin_glass_coinfection_model.py # Spin glass CNS coinfection dynamics simulation
│   └── clinvar_viral_susceptibility_analysis.py # ClinVar host-genetic viral risk analysis
├── figures/
│   ├── spin_glass_phase_diagram.csv
│   ├── spin_glass_frustration_landscape.csv
│   ├── clinvar_pathway_enrichment.csv
│   ├── host_genetic_predisposition_scores.csv
│   ├── clinvar_association_summary.csv
│   └── host_genetic_viral_network.graphml
└── REFERENCES.md                       # Bibliography & citations
```

## Reproducible local pipeline

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=app/backend python -m pytest -q
python analysis/spin_glass_coinfection_model.py
python analysis/clinvar_viral_susceptibility_analysis.py
cd app/frontend && npm ci && npm run build && cd ../..
```

The analysis outputs in `figures/` are deterministic with fixed random seeds and should regenerate without diffs.

## Manuscript and preprint drafting workflow

The current integrated repository state supports **manuscript drafting and preprint preparation**, but it should **not** be represented as final journal-submission-ready without completing citation verification, author metadata, journal formatting, and domain review.

1. Regenerate the deterministic analysis artifacts with the commands above.
2. Draft from `/home/runner/work/herpes-neurotropic-ms-research/herpes-neurotropic-ms-research/manuscript/manuscript.md`.
3. Use the figure/table inventory and claim traceability sections in the manuscript to connect text to repository artifacts and `REFERENCES.md`.
4. Replace every placeholder marked as requiring author or journal decisions before external submission.
5. Keep the application framed as research/decision-support software; it is not a diagnostic device or clinically validated model.

## Interactive MS Risk Web App

An interactive risk scoring web application is available under `app/` with:

- Viral profile inputs (HSV-1, HHV-6, EBV, CMV) and titer levels
- ClinVar variant search and risk allele accumulation
- Real-time risk score, credible interval, and contribution radar plot
- Spin-glass coinfection state and phase-diagram summary
- Scenario simulation and PDF/JSON/CSV export

See `app/README.md` for local setup, Docker usage, and API documentation.

> **Safety framing:** All model outputs are research/decision-support artifacts and are **not** clinical diagnosis.

## Document Sections

### 1. Viral Epidemiology
- EBV, CMV, HSV-1, HHV-6 prevalence in MS cohorts
- Seroprevalence studies and MS risk association
- Geographic variation and genetic susceptibility

### 2. Viral Pathogenesis
- CNS tropism mechanisms
- Latency & reactivation cycles
- Neuroinflammation pathways
- Bystander tissue damage

### 3. Coinfection Dynamics
- Viral interference and synergism
- Cross-reactive immune responses
- Altered viral replication in coinfection
- Compartmentalization in the CNS

### 4. Autoimmunity Mechanisms
- Molecular mimicry between viral and myelin proteins
- Bystander activation of autoreactive T cells
- Epitope spreading
- Loss of immune tolerance

### 5. MS Pathogenesis Links
- Demyelination triggers
- BBB breakdown
- T cell infiltration
- Oligodendrocyte dysfunction

## Contributing

This is an evolving deep review. Please contribute by:
1. Adding research findings to relevant sections
2. Updating with newly published studies
3. Creating issues for research questions or gaps
4. Submitting pull requests with additions or corrections

## References

See `REFERENCES.md` for the complete bibliography organized by topic.

---

**Last Updated:** September 2026
**Maintainer:** SivaKoganti