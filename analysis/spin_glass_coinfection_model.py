#!/usr/bin/env python3
"""Spin glass model for viral coinfection dynamics in CNS compartments."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import numpy as np
import pandas as pd

SPIN_STATES = np.array([-1, 0, 1])  # latent, cleared, replicating


@dataclass(frozen=True)
class SpinGlassConfig:
    """Model configuration for a viral coinfection spin system."""

    viruses: Tuple[str, ...] = ("HSV1", "HHV6", "EBV", "CMV")
    compartments: Tuple[str, ...] = ("grey_matter", "white_matter_lesion", "csf")
    immune_pressure: float = 0.7
    rng_seed: int = 7
    burn_in: int = 300
    samples: int = 400


def _default_couplings(viruses: Iterable[str]) -> pd.DataFrame:
    """Create a symmetric coupling matrix (J_ij) for viral interactions."""

    v = list(viruses)
    matrix = np.array(
        [
            [0.0, 0.4, 0.2, -0.2],
            [0.4, 0.0, 0.3, 0.1],
            [0.2, 0.3, 0.0, -0.1],
            [-0.2, 0.1, -0.1, 0.0],
        ]
    )
    return pd.DataFrame(matrix[: len(v), : len(v)], index=v, columns=v)


def _compartment_fields(compartments: Iterable[str], burden_shift: float = 0.0) -> Dict[str, float]:
    """External field values (h_i) for tissue compartment viral permissiveness."""

    baseline = {"grey_matter": 0.35, "white_matter_lesion": 0.55, "csf": 0.2}
    return {c: baseline.get(c, 0.25) + burden_shift for c in compartments}


def hamiltonian(
    spins: np.ndarray,
    couplings: np.ndarray,
    fields: np.ndarray,
    immune_pressure: float,
) -> float:
    """H = -sum_ij J_ij s_i s_j - sum_i h_i s_i + immune_pressure_term."""

    pair_term = 0.0
    field_term = 0.0
    immune_term = 0.0

    n_sites, n_viruses = spins.shape
    for site in range(n_sites):
        s = spins[site]
        pair_term += -0.5 * float(s @ couplings @ s)
        field_term += -float(fields[site] * np.sum(s))
        immune_term += immune_pressure * float(np.sum(np.maximum(s, 0)))
    return pair_term + field_term + immune_term


def _frustration_index(spins: np.ndarray, couplings: np.ndarray) -> float:
    """Fraction of non-zero pairwise interactions that are energetically unsatisfied."""

    unsatisfied = 0
    total = 0
    _, n_viruses = spins.shape
    for site_spins in spins:
        for i in range(n_viruses):
            for j in range(i + 1, n_viruses):
                if couplings[i, j] == 0 or site_spins[i] == 0 or site_spins[j] == 0:
                    continue
                total += 1
                if couplings[i, j] * site_spins[i] * site_spins[j] < 0:
                    unsatisfied += 1
    return float(unsatisfied / total) if total else 0.0


def _replica_order_parameter(samples: np.ndarray) -> float:
    """Edwards-Anderson-like order parameter q = mean(<s_i>^2)."""

    if len(samples) == 0:
        return 0.0
    local_means = np.mean(samples, axis=0)
    return float(np.mean(local_means**2))


def metropolis_simulation(
    config: SpinGlassConfig,
    temperature: float,
    burden_shift: float = 0.0,
) -> Dict[str, float]:
    """Simulate viral spin dynamics and summarize metastable/steady behavior."""

    rng = np.random.default_rng(config.rng_seed)
    n_sites = len(config.compartments)
    n_viruses = len(config.viruses)
    couplings_df = _default_couplings(config.viruses)
    couplings = couplings_df.to_numpy()
    fields = np.array([_compartment_fields(config.compartments, burden_shift)[c] for c in config.compartments])

    spins = rng.choice(SPIN_STATES, size=(n_sites, n_viruses))
    sampled_states: List[np.ndarray] = []

    total_steps = config.burn_in + config.samples
    for step in range(total_steps):
        site = int(rng.integers(0, n_sites))
        virus = int(rng.integers(0, n_viruses))
        current_state = spins[site, virus]
        proposal_choices = SPIN_STATES[SPIN_STATES != current_state]
        proposal = int(rng.choice(proposal_choices))

        current_energy = hamiltonian(spins, couplings, fields, config.immune_pressure)
        spins[site, virus] = proposal
        proposed_energy = hamiltonian(spins, couplings, fields, config.immune_pressure)
        delta = proposed_energy - current_energy
        if delta > 0 and rng.random() > np.exp(-delta / max(temperature, 1e-6)):
            spins[site, virus] = current_state

        if step >= config.burn_in:
            sampled_states.append(spins.copy())

    sample_arr = np.array(sampled_states)
    mean_replication = float(np.mean(np.maximum(sample_arr, 0))) if len(sample_arr) else 0.0
    mean_latency = float(np.mean(sample_arr == -1)) if len(sample_arr) else 0.0
    final_energy = hamiltonian(spins, couplings, fields, config.immune_pressure)

    return {
        "temperature": temperature,
        "burden_shift": burden_shift,
        "mean_replication": mean_replication,
        "mean_latency": mean_latency,
        "frustration_index": _frustration_index(spins, couplings),
        "replica_q": _replica_order_parameter(sample_arr),
        "final_energy": final_energy,
    }


def run_phase_scan(
    out_dir: Path,
    config: SpinGlassConfig | None = None,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Generate phase/frustration outputs across temperature and burden grid."""

    cfg = config or SpinGlassConfig()
    temperatures = np.linspace(0.4, 3.0, 8)
    burden_grid = np.linspace(-0.2, 0.4, 7)

    results = []
    for temp in temperatures:
        for burden in burden_grid:
            summary = metropolis_simulation(cfg, float(temp), float(burden))
            summary["reactivation_cascade_risk"] = (
                summary["mean_replication"] * (1.0 + summary["frustration_index"])
            )
            results.append(summary)

    phase_df = pd.DataFrame(results).sort_values(["temperature", "burden_shift"]).reset_index(drop=True)
    frustration_df = phase_df[
        [
            "temperature",
            "burden_shift",
            "frustration_index",
            "replica_q",
            "reactivation_cascade_risk",
            "final_energy",
        ]
    ].copy()

    out_dir.mkdir(parents=True, exist_ok=True)
    phase_df.to_csv(out_dir / "spin_glass_phase_diagram.csv", index=False)
    frustration_df.to_csv(out_dir / "spin_glass_frustration_landscape.csv", index=False)
    return phase_df, frustration_df


if __name__ == "__main__":
    repository_root = Path(__file__).resolve().parents[1]
    figure_dir = repository_root / "figures"
    phase, frustration = run_phase_scan(figure_dir)
    print(f"Wrote {len(phase)} phase rows to {figure_dir / 'spin_glass_phase_diagram.csv'}")
    print(
        "Wrote frustration landscape to "
        f"{figure_dir / 'spin_glass_frustration_landscape.csv'}"
    )
