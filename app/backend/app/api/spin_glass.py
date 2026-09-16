from app.models.schemas import ViralProfile
from app.services.spin_glass import evaluate_spin_glass_state


def get_coinfection_state(payload: ViralProfile) -> dict[str, float | str]:
    return evaluate_spin_glass_state(payload)
