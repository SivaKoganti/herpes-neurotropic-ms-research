from app.models.schemas import ViralProfile


def _titer_score(level: str) -> float:
    return {"low": 0.2, "medium": 0.5, "high": 0.9}[level]


def evaluate_spin_glass_state(viral_profile: ViralProfile) -> dict[str, float | str]:
    viruses = [viral_profile.hsv1, viral_profile.hhv6, viral_profile.ebv, viral_profile.cmv]
    active = sum(1 for v in viruses if v)
    titer_pressure = (
        _titer_score(viral_profile.titer_hsv1.value)
        + _titer_score(viral_profile.titer_hhv6.value)
        + _titer_score(viral_profile.titer_ebv.value)
        + _titer_score(viral_profile.titer_cmv.value)
    ) / 4
    frustration = round(min(1.0, (active / 4) * 0.7 + titer_pressure * 0.3), 3)
    energy = round(-1.0 * active + (frustration * 0.5), 3)
    metastable_occupancy = round(min(1.0, 0.15 + frustration * 0.7), 3)
    stable_pattern = {1: "single", 2: "dual", 3: "triple", 4: "quad"}.get(active, "none")
    return {
        "energy": energy,
        "frustration": frustration,
        "metastable_occupancy": metastable_occupancy,
        "stable_pattern": stable_pattern,
    }


def phase_diagram_points() -> list[dict[str, float | str]]:
    points: list[dict[str, float | str]] = []
    for reactivation in [0.1, 0.3, 0.5, 0.7, 0.9]:
        for tropism in [0.1, 0.3, 0.5, 0.7, 0.9]:
            frustration = round((reactivation * 0.6 + tropism * 0.4), 3)
            state = "stable" if frustration < 0.45 else "metastable" if frustration < 0.75 else "unstable"
            points.append(
                {
                    "reactivation_rate": reactivation,
                    "cns_tropism": tropism,
                    "frustration": frustration,
                    "state": state,
                }
            )
    return points
