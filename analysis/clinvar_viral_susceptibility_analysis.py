#!/usr/bin/env python3
"""ClinVar-host-viral susceptibility integration for MS-focused analyses."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import networkx as nx
import numpy as np
import pandas as pd
from scipy.stats import fisher_exact
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_predict

GENE_SETS: Dict[str, List[str]] = {
    "HLA": ["HLA-DRB1", "HLA-DQA1", "HLA-A", "HLA-B"],
    "TLR_PRR": ["TLR3", "TLR7", "TLR9", "IFIH1"],
    "TYPE_I_IFN": ["IFNAR1", "IFNAR2", "IRF7", "STAT1", "STAT2"],
    "T_CELL_REGULATORS": ["IL2RA", "IL7R", "CTLA4", "TNFRSF1A"],
}


def _normalize_binary_column(df: pd.DataFrame, column: str) -> pd.Series:
    values = pd.to_numeric(df[column], errors="coerce")
    if values.isna().any():
        raise ValueError(f"Column '{column}' contains non-numeric or missing values.")
    invalid = sorted(set(values.astype(int).unique()) - {0, 1})
    if invalid:
        raise ValueError(f"Column '{column}' must be binary 0/1 values. Found: {invalid}")
    return values.astype(int)


def load_clinvar_subset(path: Path) -> pd.DataFrame:
    """Load filtered ClinVar subset used in host susceptibility analysis."""

    df = pd.read_csv(path)
    required = {
        "variant_id",
        "gene",
        "clinical_significance",
        "ms_association",
        "viral_seropositive",
        "viral_persistence",
        "reactivation",
    }
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required ClinVar columns: {sorted(missing)}")
    normalized = (
        df["clinical_significance"]
        .fillna("")
        .str.lower()
        .str.replace("-", " ", regex=False)
        .str.strip()
    )
    df["is_pathogenic"] = normalized.isin({"pathogenic", "likely pathogenic"})
    for binary_col in ("ms_association", "viral_seropositive", "viral_persistence", "reactivation"):
        df[binary_col] = _normalize_binary_column(df, binary_col)
    return df


def annotate_pathways(df: pd.DataFrame) -> pd.DataFrame:
    """Annotate each variant into immune pathway buckets."""

    annotated = df.copy()
    annotated["pathway"] = "OTHER"
    for pathway, genes in GENE_SETS.items():
        annotated.loc[annotated["gene"].isin(genes), "pathway"] = pathway
    return annotated


def pathway_enrichment(df: pd.DataFrame) -> pd.DataFrame:
    """Fisher exact enrichment of viral persistence by pathway membership.

    Returns persistence contingency counts, odds ratio/p-value, and pathway-level
    pathogenic/reactivation fractions for interpretation.
    """

    rows = []
    persistent_values = _normalize_binary_column(df, "viral_persistence")
    for pathway in sorted(df["pathway"].unique()):
        in_pathway = df["pathway"] == pathway
        persistent = persistent_values == 1
        non_persistent = persistent_values == 0
        a = int((in_pathway & persistent).sum())
        b = int((in_pathway & non_persistent).sum())
        c = int(((~in_pathway) & persistent).sum())
        d = int(((~in_pathway) & non_persistent).sum())
        odds_ratio, p_value = fisher_exact([[a, b], [c, d]], alternative="greater")
        rows.append(
            {
                "pathway": pathway,
                "persistent_in_pathway": a,
                "non_persistent_in_pathway": b,
                "persistent_outside_pathway": c,
                "non_persistent_outside_pathway": d,
                "pathway_pathogenic_fraction": float(df.loc[in_pathway, "is_pathogenic"].mean()),
                "pathway_reactivation_fraction": float(df.loc[in_pathway, "reactivation"].mean()),
                "odds_ratio": float(odds_ratio),
                "p_value": float(p_value),
            }
        )
    return pd.DataFrame(rows).sort_values("p_value").reset_index(drop=True)


def logistic_reactivation_model(df: pd.DataFrame) -> pd.DataFrame:
    """Estimate genotype-linked reactivation risk using logistic regression."""

    feature_cols = ["is_pathogenic", "ms_association"]
    pathway_dummies = pd.get_dummies(df["pathway"], prefix="pathway", drop_first=True)
    design = pd.concat([df[feature_cols].astype(float), pathway_dummies.astype(float)], axis=1)
    design = design.loc[:, design.nunique(dropna=False) > 1]
    target = df["reactivation"].astype(int)

    if target.nunique() < 2:
        probabilities = np.full(len(target), float(target.mean()))
        score_mode = "constant_single_class"
    else:
        class_counts = target.value_counts()
        min_class = int(class_counts.min()) if not class_counts.empty else 0
        if min_class >= 2:
            n_splits = min(5, min_class)
            cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=7)
            model = LogisticRegression(max_iter=1000, solver="liblinear")
            probabilities = cross_val_predict(
                model,
                design,
                target,
                cv=cv,
                method="predict_proba",
            )[:, 1]
            score_mode = "cross_validated"
        else:
            model = LogisticRegression(max_iter=1000, solver="liblinear")
            model.fit(design, target)
            probabilities = model.predict_proba(design)[:, 1]
            score_mode = "in_sample_fallback"

    score_df = df[
        ["variant_id", "gene", "clinical_significance", "pathway", "reactivation"]
    ].copy()
    score_df["predicted_reactivation_risk"] = probabilities
    score_df["host_genetic_predisposition_score"] = (
        probabilities
        * (
            1.0
            + 0.5 * df["is_pathogenic"].astype(float)
            + 0.25 * df["ms_association"].astype(float)
        )
    )
    score_df["score_mode"] = score_mode
    return score_df.sort_values(
        "host_genetic_predisposition_score", ascending=False
    ).reset_index(drop=True)


def permutation_association_test(df: pd.DataFrame, n_perm: int = 500, rng_seed: int = 7) -> float:
    """Permutation p-value for pathogenic burden association with reactivation."""

    rng = np.random.default_rng(rng_seed)
    reactivation_values = _normalize_binary_column(df, "reactivation").to_numpy()
    pathogenic_mask = df["is_pathogenic"].astype(bool).to_numpy()
    non_pathogenic_mask = ~pathogenic_mask
    if pathogenic_mask.sum() == 0 or non_pathogenic_mask.sum() == 0:
        raise ValueError("Permutation test requires both pathogenic and non-pathogenic groups.")
    observed = float(
        np.mean(reactivation_values[pathogenic_mask])
        - np.mean(reactivation_values[non_pathogenic_mask])
    )
    count = 0
    for _ in range(n_perm):
        perm = rng.permutation(reactivation_values)
        perm_diff = float(np.mean(perm[pathogenic_mask]) - np.mean(perm[non_pathogenic_mask]))
        if abs(perm_diff) >= abs(observed):
            count += 1
    return (count + 1) / (n_perm + 1)


def build_correlation_network(df: pd.DataFrame) -> nx.Graph:
    """Construct host-genetic-viral-outcome association network."""

    graph = nx.Graph()
    graph.add_node("viral_persistence", node_type="outcome")
    graph.add_node("reactivation", node_type="outcome")
    graph.add_node("ms_association", node_type="outcome")

    for pathway in sorted(df["pathway"].unique()):
        graph.add_node(pathway, node_type="pathway")
        subset = df[df["pathway"] == pathway]
        graph.add_edge(pathway, "viral_persistence", weight=float(subset["viral_persistence"].mean()))
        graph.add_edge(pathway, "reactivation", weight=float(subset["reactivation"].mean()))
        graph.add_edge(pathway, "ms_association", weight=float(subset["ms_association"].mean()))

    for gene in sorted(df["gene"].unique()):
        gene_subset = df[df["gene"] == gene]
        pathway = gene_subset["pathway"].iloc[0]
        graph.add_node(gene, node_type="gene")
        graph.add_edge(gene, pathway, weight=float(gene_subset["is_pathogenic"].mean()))
    return graph


def run_analysis(clinvar_csv: Path, output_dir: Path) -> None:
    """Run end-to-end ClinVar host susceptibility workflow."""

    df = annotate_pathways(load_clinvar_subset(clinvar_csv))
    enrichment = pathway_enrichment(df)
    scores = logistic_reactivation_model(df)
    permutation_p = permutation_association_test(df)
    network = build_correlation_network(df)

    output_dir.mkdir(parents=True, exist_ok=True)
    enrichment.to_csv(output_dir / "clinvar_pathway_enrichment.csv", index=False)
    scores.to_csv(output_dir / "host_genetic_predisposition_scores.csv", index=False)
    nx.write_graphml(network, output_dir / "host_genetic_viral_network.graphml")

    summary = pd.DataFrame(
        {
            "metric": ["permutation_p_value", "n_variants", "n_pathogenic"],
            "value": [permutation_p, len(df), int(df["is_pathogenic"].sum())],
        }
    )
    summary.to_csv(output_dir / "clinvar_association_summary.csv", index=False)


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parents[1]
    clinvar_file = repo_root / "data" / "clinvar-ms-variants.csv"
    figures_dir = repo_root / "figures"
    run_analysis(clinvar_file, figures_dir)
    print(f"Wrote ClinVar susceptibility outputs to {figures_dir}")
