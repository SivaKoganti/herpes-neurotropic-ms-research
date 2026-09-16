# Interactive MS Risk Score Application

This application adds an interactive dashboard and FastAPI backend for exploratory MS risk stratification from viral coinfection and host ClinVar genetic features.

> This software is for research and decision-support workflows. It does **not** provide clinical diagnosis.

## Architecture

- `frontend/`: React + TypeScript dashboard
- `backend/`: FastAPI API for risk scoring, spin-glass state, ClinVar variant query, phase diagrams, scenario simulation, and PDF report generation
- `docker-compose.yml` (repo root): local stack with frontend, backend, PostgreSQL, and Redis

## Backend setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --app-dir app/backend
```

API docs: `http://localhost:8000/docs`

## Frontend setup

```bash
cd app/frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

Set `VITE_API_BASE_URL` if the backend runs on a non-default host/port.

## Validation commands

From repository root:

```bash
PYTHONPATH=app/backend python -m pytest -q
python analysis/spin_glass_coinfection_model.py
python analysis/clinvar_viral_susceptibility_analysis.py
cd app/frontend && npm ci && npm run build && cd ../..
```

## Manuscript and preprint use

- Use `/home/runner/work/herpes-neurotropic-ms-research/herpes-neurotropic-ms-research/manuscript/manuscript.md` as the publication draft anchor for IMRaD text, figure legends, inventory tables, and claim traceability.
- Regenerate repository artifacts before updating manuscript text so the inventory continues to match the tracked outputs in `figures/`.
- Treat dashboard exports and API reports as exploratory research artifacts only. They may be used to illustrate the repository workflow, but they must not be described as clinical diagnosis, clinical validation, or patient-ready reporting.
- Author list, affiliations, target venue, and any claim marked as requiring verification remain placeholders until completed by the manuscript authors.

## Docker Compose

```bash
docker compose up --build
```

## Export and privacy

- Dashboard supports PDF/JSON/CSV export of computed risk outputs.
- Use anonymized patient identifiers unless explicit consent for identifiable storage is available.
