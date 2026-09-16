from app.models.schemas import RiskScoreRequest
from app.services.risk_calculator import calculate_risk


def compute_risk(payload: RiskScoreRequest) -> dict:
    return calculate_risk(payload)
