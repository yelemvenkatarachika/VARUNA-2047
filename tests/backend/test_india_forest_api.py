"""
VARUNA 2047 - Tests for India GIS & ForestWatch Endpoints
Verifies:
- GET /api/india/states
- GET /api/india/states/{state_id}
- GET /api/india/states/{state_id}/districts
- GET /api/india/districts/{district_id}
- GET /api/forest/coverage
- GET /api/forest/change
- GET /api/forest/loss/history
- GET /api/forest/loss/regions
- GET /api/forest/satellite-scenes
- GET /api/forest/change-map
- GET /api/forest/provenance
- POST /api/forest/compare
- POST /api/forest/reports/generate
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_india_states_endpoint():
    response = client.get("/api/india/states")
    assert response.status_code == 200
    data = response.json()
    assert data["total_states"] == 36
    assert "geojson" in data
    assert len(data["geojson"]["features"]) == 36

def test_india_state_detail():
    response = client.get("/api/india/states/TS")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Telangana"
    assert data["capital"] == "Hyderabad"

def test_india_state_districts():
    response = client.get("/api/india/states/TS/districts")
    assert response.status_code == 200
    data = response.json()
    assert data["state_id"] == "TS"
    assert data["total_districts"] >= 6

def test_india_district_detail():
    response = client.get("/api/india/districts/WAR")
    assert response.status_code == 200
    data = response.json()
    assert "Warangal" in data["name"]
    assert data["state_id"] == "TS"

def test_forest_coverage():
    response = client.get("/api/forest/coverage")
    assert response.status_code == 200
    data = response.json()
    assert data["national_forest_cover_pct"] == 21.71
    assert data["states_count"] == 36

def test_forest_change_national():
    response = client.get("/api/forest/change?region_id=NATIONAL")
    assert response.status_code == 200
    data = response.json()
    assert data["region_id"] == "NATIONAL"
    assert "trajectory" in data
    assert data["data_confidence"] >= 0.90

def test_forest_change_district():
    response = client.get("/api/forest/change?region_id=WAR")
    assert response.status_code == 200
    data = response.json()
    assert data["region_id"] == "WAR"
    assert data["latest_annual_loss_ha"] > 0

def test_forest_loss_history():
    response = client.get("/api/forest/loss/history?region_id=NATIONAL")
    assert response.status_code == 200
    data = response.json()
    assert "history" in data
    assert "2023" in data["history"]

def test_forest_loss_regions():
    response = client.get("/api/forest/loss/regions?region_type=states&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    assert "loss_2023_ha" in data[0]

def test_forest_satellite_scenes():
    response = client.get("/api/forest/satellite-scenes")
    assert response.status_code == 200
    data = response.json()
    assert "WAR_FOREST_CORRIDOR" in data
    assert "Sentinel-2" in data["WAR_FOREST_CORRIDOR"]["baseline_scene"]["mission"]

def test_forest_change_map():
    response = client.get("/api/forest/change-map")
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "FeatureCollection"
    assert len(data["features"]) == 36

def test_forest_provenance():
    response = client.get("/api/forest/provenance")
    assert response.status_code == 200
    data = response.json()
    assert "fsi_isfr" in data
    assert "hansen_gfc" in data

def test_forest_compare_post():
    payload = {
        "region_id": "WAR",
        "baseline_year": 2019,
        "recent_year": 2023,
        "canopy_class": "OF"
    }
    response = client.post("/api/forest/compare", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["region_id"] == "WAR"
    assert data["loss_area_ha"] > 0
    # In accordance with Priority 4, tree count estimation from satellite pixels without LiDAR/ground plots is disabled
    assert data["tree_count_available"] is False
    assert data["estimated_trees_lost"] is None
    assert data["reproduction_status"] == "VERIFIED_COPERNICUS_L2A_PROCESSED"
    assert "visual_assets" in data

def test_forest_report_generate():
    payload = {
        "region_id": "WAR",
        "region_type": "district",
        "include_satellite_comparison": True
    }
    response = client.post("/api/forest/reports/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "download_url" in data
    assert data["status"] == "READY"
