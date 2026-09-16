import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = REPO_ROOT / "manuscript" / "manuscript.md"
REFERENCES = REPO_ROOT / "REFERENCES.md"


class ManuscriptAssetTests(unittest.TestCase):
    def test_manuscript_contains_required_sections(self) -> None:
        text = MANUSCRIPT.read_text(encoding="utf-8")
        required_sections = [
            "## Abstract",
            "## Introduction",
            "## Research Questions",
            "## Methods",
            "## Results and reporting of generated artifacts",
            "## Discussion",
            "## Limitations",
            "## Reproducibility",
            "## Ethics and safety framing",
            "## Figure legends",
            "## Figure and table inventory",
            "## Claim traceability",
            "## References",
        ]
        for section in required_sections:
            self.assertIn(section, text)

    def test_manuscript_inventory_references_existing_repository_assets(self) -> None:
        text = MANUSCRIPT.read_text(encoding="utf-8")
        expected_paths = [
            "analysis/spin_glass_coinfection_model.py",
            "analysis/clinvar_viral_susceptibility_analysis.py",
            "data/clinvar-ms-variants.csv",
            "figures/spin_glass_phase_diagram.csv",
            "figures/spin_glass_frustration_landscape.csv",
            "figures/clinvar_pathway_enrichment.csv",
            "figures/host_genetic_predisposition_scores.csv",
            "figures/clinvar_association_summary.csv",
            "figures/host_genetic_viral_network.graphml",
            "app/backend/app/services/report_generator.py",
        ]
        for relative_path in expected_paths:
            self.assertIn(relative_path, text)
            self.assertTrue((REPO_ROOT / relative_path).exists(), relative_path)

    def test_traceability_reference_keys_exist_in_references_index(self) -> None:
        manuscript_text = MANUSCRIPT.read_text(encoding="utf-8")
        references_text = REFERENCES.read_text(encoding="utf-8")
        keys = sorted(set(re.findall(r"REF-[A-Z0-9-]+", manuscript_text)))
        self.assertTrue(keys)
        for key in keys:
            self.assertIn(key, references_text)


if __name__ == "__main__":
    unittest.main()
