"""
VARUNA 2047 - Backend Automated Test Suite
Tests all core API endpoints using FastAPI TestClient:
- Health
- Data sources & provenance
- Districts listing & detail
- ENSO history & current state
- Rainfall history & anomalies
- Satellite layers
- Model registry & metrics
- Risk prediction inference
- Resilience prioritization
- Evidence report generation
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["project"] == "VARUNA 2047"
    assert data["datasets_ready"] is True
    assert data["models_ready"] is True

def test_data_sources_endpoint():
    response = client.get("/api/data/sources")
    assert response.status_code == 200
    data = response.json()
    assert "provenance_registry" in data
    assert len(data["provenance_registry"]) >= 4
    # Check that ISRO Bhuvan is documented
    providers = [s["provider"] for s in data["provenance_registry"]]
    assert any("ISRO" in p for p in providers)

def test_districts_endpoint():
    response = client.get("/api/districts")
    assert response.status_code == 200
    data = response.json()
    assert "districts" in data
    assert "geojson" in data
    assert len(data["districts"]) == 6
    # Verify pilot districts present
    d_ids = [d["id"] for d in data["districts"]]
    assert "WAR" in d_ids
    assert "HAN" in d_ids
    assert "ADI" in d_ids

def test_district_detail_valid():
    response = client.get("/api/districts/WAR")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Warangal"
    assert data["elevation_m"] == 280

def test_district_detail_invalid():
    response = client.get("/api/districts/INVALID_ID")
    assert response.status_code == 404

def test_enso_endpoints():
    r_hist = client.get("/api/enso/history")
    assert r_hist.status_code == 200
    hist = r_hist.json()
    assert len(hist["data"]) >= 900

    r_curr = client.get("/api/enso/current")
    assert r_curr.status_code == 200
    curr = r_curr.json()
    assert "latest_observation" in curr

    r_events = client.get("/api/enso/events")
    assert r_events.status_code == 200
    events = r_events.json()
    assert len(events["events"]) >= 30

def test_rainfall_endpoints():
    r_rf = client.get("/api/rainfall/history?district_id=WAR")
    assert r_rf.status_code == 200
    data = r_rf.json()
    assert data["district_id"] == "WAR"
    assert data["climatological_normal_jjas_mm"] > 0

    r_anom = client.get("/api/rainfall/anomalies?district_id=WAR")
    assert r_anom.status_code == 200
    anom_list = r_anom.json()
    assert len(anom_list) >= 40

def test_satellite_layers():
    response = client.get("/api/satellite/layers")
    assert response.status_code == 200
    data = response.json()
    assert len(data["layers"]) >= 3
    # Check that live ISRO Bhuvan WMS is in layers
    layer_ids = [l["id"] for l in data["layers"]]
    assert "isro_bhuvan_wms" in layer_ids

def test_models_and_metrics():
    r_models = client.get("/api/models")
    assert r_models.status_code == 200
    models_data = r_models.json()
    assert len(models_data["models"]) >= 4

    r_metrics = client.get("/api/models/model_b_enso_lr/metrics")
    assert r_metrics.status_code == 200
    metrics = r_metrics.json()
    assert "roc_auc" in metrics["metrics"]

def test_risk_predict_endpoint():
    payload = {
        "district_id": "WAR",
        "model_id": "model_b_enso_lr",
        "nino34_mam": 1.5,
        "nino34_trend": 0.5,
        "preseason_mam_rainfall_mm": 35.0,
        "preseason_may_ndvi": 0.22
    }
    response = client.post("/api/risk/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["district_id"] == "WAR"
    assert 0.0 <= data["deficit_probability"] <= 1.0
    assert len(data["primary_drivers"]) >= 3

def test_resilience_prioritize_endpoint():
    payload = {
        "risk_weight": 0.40,
        "vegetation_stress_weight": 0.20,
        "exposure_weight": 0.20,
        "irrigation_vulnerability_weight": 0.20,
        "year": 2024
    }
    response = client.post("/api/resilience/prioritize", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["ranked_districts"]) == 6
    assert data["ranked_districts"][0]["priority_rank"] == 1

def test_report_generation():
    payload = {
        "district_id": "WAR",
        "year": 2024,
        "include_enso": True,
        "include_satellite": True,
        "include_recommendations": True
    }
    response = client.post("/api/reports/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "report_id" in data
    assert data["file_size_bytes"] > 1000

    # Download verification
    dl_response = client.get(data["download_url"])
    assert dl_response.status_code == 200
    assert dl_response.headers["content-type"] == "application/pdf"
