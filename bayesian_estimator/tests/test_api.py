from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_bayesian_estimate_success():
    payload = {
        "prior_alpha": 2.0,
        "prior_beta": 8.0,
        "picking_attempts": 100,
        "reported_discrepancies": 10
    }
    response = client.post("/estimate/stock-confidence", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "posterior_mean" in data
    assert "hdi_95_lower" in data
    assert "hdi_95_upper" in data
    assert data["stock_risk_category"] == "LOW_MISCOUNT_RISK"


def test_invalid_discrepancy_count():
    payload = {
        "prior_alpha": 2.0,
        "prior_beta": 8.0,
        "picking_attempts": 10,
        "reported_discrepancies": 20
    }
    response = client.post("/estimate/stock-confidence", json=payload)
    assert response.status_code == 400