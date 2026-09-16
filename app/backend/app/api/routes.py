from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from app.api.risk_scoring import compute_risk
from app.api.spin_glass import get_coinfection_state
from app.api.variant_queries import find_variant, search_variants
from app.models.schemas import (
    CoinfectionStateResponse,
    PhaseDiagramResponse,
    ReportRequest,
    RiskScoreRequest,
    RiskScoreResponse,
    ScenarioCompareRequest,
    ScenarioResponse,
    VariantInfoResponse,
    ViralProfile,
)
from app.services.coinfection_simulator import scenario_risk
from app.services.report_generator import generate_pdf_bytes
from app.services.spin_glass import phase_diagram_points

router = APIRouter(prefix="/api", tags=["ms-risk"])


@router.post("/risk-score", response_model=RiskScoreResponse)
def risk_score(payload: RiskScoreRequest) -> RiskScoreResponse:
    return RiskScoreResponse(**compute_risk(payload))


@router.post("/coinfection-state", response_model=CoinfectionStateResponse)
def coinfection_state(payload: ViralProfile) -> CoinfectionStateResponse:
    return CoinfectionStateResponse(**get_coinfection_state(payload))


@router.get("/variant-info", response_model=list[VariantInfoResponse])
def variant_info(gene: str | None = None, variant: str | None = None) -> list[VariantInfoResponse]:
    if gene and variant:
        hit = find_variant(gene, variant)
        if not hit:
            raise HTTPException(status_code=404, detail="Variant not found")
        return [hit]
    return search_variants(gene)


@router.get("/phase-diagram", response_model=PhaseDiagramResponse)
def phase_diagram() -> PhaseDiagramResponse:
    return PhaseDiagramResponse(points=phase_diagram_points())


@router.post("/scenario-simulate", response_model=ScenarioResponse)
def scenario_simulate(payload: ScenarioCompareRequest) -> ScenarioResponse:
    baseline_risk, baseline_frustration = scenario_risk(payload.baseline)
    intervention_risk, intervention_frustration = scenario_risk(payload.intervention)
    return ScenarioResponse(
        baseline_risk=baseline_risk,
        intervention_risk=intervention_risk,
        delta=round(intervention_risk - baseline_risk, 2),
        frustration_shift=round(intervention_frustration - baseline_frustration, 3),
    )


@router.post("/generate-report")
def generate_report(payload: ReportRequest) -> Response:
    pdf_bytes = generate_pdf_bytes(payload)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={payload.patient_id}-ms-risk-report.pdf"},
    )
