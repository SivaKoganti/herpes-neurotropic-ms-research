import math

from app.models.schemas import RiskScoreRequest
from app.services.spin_glass import evaluate_spin_glass_state

PATHOGENICITY_WEIGHTS = {
    "benign": 0.0,
    "likely-benign": 0.05,
    "vus": 0.15,
    "likely-pathogenic": 0.35,
    "pathogenic": 0.5,
}


def _coinfection_term(active_count: int) -> float:
    if active_count <= 1:
        return 0.05
    if active_count == 2:
        return 0.18
    if active_count == 3:
        return 0.30
    return 0.45


def calculate_risk(request: RiskScoreRequest) -> dict:
    profile = request.viral_profile
    active_count = sum([profile.hsv1, profile.hhv6, profile.ebv, profile.cmv])

    genetic_term = sum(
        PATHOGENICITY_WEIGHTS.get(v.clinvar_pathogenicity.lower(), 0.1)
        for v in request.variants
    )
    viral_term = _coinfection_term(active_count)
    interaction_term = viral_term * min(1.0, genetic_term)

    spin_state = evaluate_spin_glass_state(profile)
    frustration = float(spin_state["frustration"])

    # prior prevalence approx 0.3%
    prior_logit = math.log(0.003 / (1 - 0.003))
    linear = prior_logit + viral_term * 2.8 + genetic_term * 1.9 + interaction_term * 1.5 + frustration * 1.3
    posterior = 1 / (1 + math.exp(-linear))

    risk_score = round(posterior * 100, 2)
    ci_width = max(2.5, 15 - active_count * 2 - min(8, len(request.variants)))
    lower = round(max(0.0, risk_score - ci_width), 2)
    upper = round(min(100.0, risk_score + ci_width), 2)

    severity = "low" if risk_score < 20 else "moderate" if risk_score < 50 else "high"
    return {
        "risk_score": risk_score,
        "severity": severity,
        "credible_interval": (lower, upper),
        "contributions": {
            "coinfection_pattern": round(viral_term * 100 / 4, 2),
            "genetic_variants": round(genetic_term * 100 / 4, 2),
            "immune_frustration": round(frustration * 100 / 4, 2),
            "interaction": round(interaction_term * 100 / 4, 2),
        },
    }
