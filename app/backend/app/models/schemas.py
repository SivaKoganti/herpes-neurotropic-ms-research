from enum import Enum

from pydantic import BaseModel, Field


class TiterLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class ViralProfile(BaseModel):
    hsv1: bool
    hhv6: bool
    ebv: bool
    cmv: bool
    titer_hsv1: TiterLevel = TiterLevel.low
    titer_hhv6: TiterLevel = TiterLevel.low
    titer_ebv: TiterLevel = TiterLevel.low
    titer_cmv: TiterLevel = TiterLevel.low


class GeneticVariantInput(BaseModel):
    gene: str
    variant: str
    clinvar_pathogenicity: str


class RiskScoreRequest(BaseModel):
    viral_profile: ViralProfile
    variants: list[GeneticVariantInput] = Field(default_factory=list)


class RiskScoreResponse(BaseModel):
    risk_score: float
    severity: str
    credible_interval: tuple[float, float]
    contributions: dict[str, float]


class CoinfectionStateResponse(BaseModel):
    energy: float
    frustration: float
    metastable_occupancy: float
    stable_pattern: str


class VariantInfoResponse(BaseModel):
    gene: str
    variant: str
    pathogenicity: str
    effect_size: float


class PhaseDiagramResponse(BaseModel):
    points: list[dict[str, float | str]]


class ScenarioInput(BaseModel):
    reactivation_rate: float = Field(ge=0.0, le=1.0)
    cns_tropism: float = Field(ge=0.0, le=1.0)
    immune_suppression: float = Field(ge=0.0, le=1.0)
    antiviral_therapy: float = Field(ge=0.0, le=1.0)


class ScenarioCompareRequest(BaseModel):
    baseline: ScenarioInput
    intervention: ScenarioInput


class ScenarioResponse(BaseModel):
    baseline_risk: float
    intervention_risk: float
    delta: float
    frustration_shift: float


class ReportRequest(BaseModel):
    patient_id: str
    risk_result: RiskScoreResponse
    notes: str | None = None
