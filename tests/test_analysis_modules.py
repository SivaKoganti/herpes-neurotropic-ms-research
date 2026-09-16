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
        self.assertAlmostEqual(p_value_a, 0.03482587064676617)
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
        self.assertAlmostEqual(p_value, 0.0845771144278607)

    def test_risk_scores_report_scoring_mode(self):
        dataset = REPO_ROOT / "data" / "clinvar-ms-variants.csv"
        df = clinvar.annotate_pathways(clinvar.load_clinvar_subset(dataset))
        scores = clinvar.logistic_reactivation_model(df)
        self.assertIn("score_mode", scores.columns)
        self.assertTrue((scores["score_mode"] == "cross_validated").all())

    def test_risk_scores_exercise_in_sample_fallback(self):
        fallback_df = pd.DataFrame(
            {
                "variant_id": ["v1", "v2", "v3", "v4", "v5"],
                "gene": ["HLA-DRB1", "TLR3", "STAT1", "IL2RA", "MBP"],
                "clinical_significance": [
                    "Pathogenic",
                    "Pathogenic",
                    "Likely pathogenic",
                    "Uncertain significance",
                    "Benign",
                ],
                "pathway": ["HLA", "TLR_PRR", "TYPE_I_IFN", "T_CELL_REGULATORS", "OTHER"],
                "is_pathogenic": [True, True, True, False, False],
                "ms_association": [1, 0, 0, 1, 0],
                "reactivation": [1, 1, 1, 1, 0],
            }
        )
        scores = clinvar.logistic_reactivation_model(fallback_df)
        self.assertTrue((scores["score_mode"] == "in_sample_fallback").all())

    def test_summary_artifact_matches_default_permutation_settings(self):
        dataset = REPO_ROOT / "data" / "clinvar-ms-variants.csv"
        df = clinvar.annotate_pathways(clinvar.load_clinvar_subset(dataset))
        expected = clinvar.permutation_association_test(df, n_perm=500, rng_seed=7)
        self.assertAlmostEqual(expected, 0.033932135728542916)

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
