import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(REPO_ROOT / "analysis"))

import clinvar_viral_susceptibility_analysis as clinvar  # noqa: E402
import spin_glass_coinfection_model as spin  # noqa: E402


class ClinVarAnalysisTests(unittest.TestCase):
    def test_pathogenic_classification_is_exact(self):
        dataset = REPO_ROOT / "data" / "clinvar-ms-variants.csv"
        df = clinvar.load_clinvar_subset(dataset)
        self.assertFalse(df.loc[df["clinical_significance"] == "Benign", "is_pathogenic"].any())
        self.assertFalse(
            df.loc[df["clinical_significance"] == "Uncertain significance", "is_pathogenic"].any()
        )
        self.assertTrue(df.loc[df["clinical_significance"] == "Pathogenic", "is_pathogenic"].all())

    def test_permutation_association_is_reproducible(self):
        dataset = REPO_ROOT / "data" / "clinvar-ms-variants.csv"
        df = clinvar.annotate_pathways(clinvar.load_clinvar_subset(dataset))
        p_value_a = clinvar.permutation_association_test(df, n_perm=200, rng_seed=7)
        p_value_b = clinvar.permutation_association_test(df, n_perm=200, rng_seed=7)
        self.assertGreaterEqual(p_value_a, 0.0)
        self.assertLessEqual(p_value_a, 1.0)
        self.assertAlmostEqual(p_value_a, 0.04477611940298507)
        self.assertAlmostEqual(p_value_a, p_value_b)

    def test_permutation_association_supports_negative_effect(self):
        negative_effect = np.rec.fromrecords(
            [
                (True, 0),
                (True, 0),
                (True, 0),
                (False, 1),
                (False, 1),
                (False, 1),
            ],
            names=["is_pathogenic", "reactivation"],
        )
        frame = pd.DataFrame(negative_effect)
        p_value = clinvar.permutation_association_test(frame, n_perm=200, rng_seed=7)
        self.assertAlmostEqual(p_value, 0.11442786069651742)

    def test_risk_scores_report_scoring_mode(self):
        dataset = REPO_ROOT / "data" / "clinvar-ms-variants.csv"
        df = clinvar.annotate_pathways(clinvar.load_clinvar_subset(dataset))
        scores = clinvar.logistic_reactivation_model(df)
        self.assertIn("score_mode", scores.columns)
        self.assertTrue((scores["score_mode"] == "cross_validated").all())

    def test_summary_artifact_matches_default_permutation_settings(self):
        dataset = REPO_ROOT / "data" / "clinvar-ms-variants.csv"
        df = clinvar.annotate_pathways(clinvar.load_clinvar_subset(dataset))
        expected = clinvar.permutation_association_test(df, n_perm=500, rng_seed=7)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            clinvar.run_analysis(dataset, output_dir)
            summary = pd.read_csv(output_dir / "clinvar_association_summary.csv")
            observed = float(
                summary.loc[summary["metric"] == "permutation_p_value", "value"].iloc[0]
            )
            self.assertAlmostEqual(observed, expected)


class SpinGlassModelTests(unittest.TestCase):
    def test_dynamic_couplings_support_more_than_four_viruses(self):
        viruses = ("HSV1", "HHV6", "EBV", "CMV", "JCV")
        couplings = spin._default_couplings(viruses)
        self.assertEqual(couplings.shape, (5, 5))
        self.assertTrue(np.allclose(couplings.to_numpy(), couplings.to_numpy().T))
        self.assertTrue(np.allclose(np.diag(couplings.to_numpy()), np.zeros(5)))


if __name__ == "__main__":
    unittest.main()
