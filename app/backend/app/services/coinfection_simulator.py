from app.models.schemas import ScenarioInput


def scenario_risk(s: ScenarioInput) -> tuple[float, float]:
    pressure = (s.reactivation_rate * 0.4) + (s.cns_tropism * 0.3) + (s.immune_suppression * 0.3)
    therapy_relief = s.antiviral_therapy * 0.45
    frustration = max(0.0, min(1.0, pressure - therapy_relief + 0.15))
    risk = max(0.0, min(100.0, (pressure - therapy_relief + 0.2) * 100))
    return round(risk, 2), round(frustration, 3)
