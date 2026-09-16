from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_risk_score_endpoint_returns_expected_shape() -> None:
    payload = {
        "viral_profile": {
            "hsv1": True,
            "hhv6": True,
            "ebv": True,
            "cmv": False,
            "titer_hsv1": "high",
            "titer_hhv6": "medium",
            "titer_ebv": "high",
            "titer_cmv": "low",
        },
        "variants": [
            {"gene": "IL6", "variant": "rs1800795", "clinvar_pathogenicity": "pathogenic"},
            {"gene": "STAT3", "variant": "rs744166", "clinvar_pathogenicity": "likely-pathogenic"},
        ],
    }
    resp = client.post("/api/risk-score", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert 0 <= body["risk_score"] <= 100
    assert body["severity"] in {"low", "moderate", "high"}
    assert len(body["credible_interval"]) == 2


def test_variant_info_lookup() -> None:
    resp = client.get("/api/variant-info", params={"gene": "TLR2", "variant": "rs5743708"})
    assert resp.status_code == 200
    body = resp.json()
    assert body[0]["gene"] == "TLR2"
    assert body[0]["pathogenicity"] == "likely-pathogenic"


def test_generate_report_returns_pdf() -> None:
    payload = {
        "patient_id": "PAT-001",
        "risk_result": {
            "risk_score": 34.2,
            "severity": "moderate",
            "credible_interval": [22.0, 46.3],
            "contributions": {
                "coinfection_pattern": 5.5,
                "genetic_variants": 8.2,
                "immune_frustration": 6.1,
                "interaction": 3.0,
            },
        },
    }
    resp = client.post("/api/generate-report", json=payload)
    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("application/pdf")
    assert resp.content.startswith(b"%PDF")
