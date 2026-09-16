import sys
import unittest
from pathlib import Path

import numpy as np

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


class SpinGlassModelTests(unittest.TestCase):
    def test_dynamic_couplings_support_more_than_four_viruses(self):
        viruses = ("HSV1", "HHV6", "EBV", "CMV", "JCV")
        couplings = spin._default_couplings(viruses)
        self.assertEqual(couplings.shape, (5, 5))
        self.assertTrue(np.allclose(couplings.to_numpy(), couplings.to_numpy().T))
        self.assertTrue(np.allclose(np.diag(couplings.to_numpy()), np.zeros(5)))


if __name__ == "__main__":
    unittest.main()
