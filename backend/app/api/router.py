"""
VARUNA 2047 - Backend API Router
Implements all 18 documented endpoints required by specification Section 8:
- GET  /api/health
- GET  /api/data/sources
- GET  /api/districts
- GET  /api/districts/{district_id}
- GET  /api/enso/history
- GET  /api/enso/current
- GET  /api/enso/events
- GET  /api/rainfall/history
- GET  /api/rainfall/anomalies
- GET  /api/satellite/layers
- GET  /api/satellite/metadata
- GET  /api/vegetation/history
- GET  /api/vegetation/anomalies
- GET  /api/models
- GET  /api/models/{model_id}/metrics
- GET  /api/models/{model_id}/features
- POST /api/risk/predict
- POST /api/resilience/prioritize
- POST /api/reports/generate
- GET  /api/reports/{report_id}
"""

import os
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Query, Response
from fastapi.responses import FileResponse
from backend.app.core.config import settings
from backend.app.schemas.schemas import (
    HealthResponse, PredictRiskRequest, PredictRiskResponse,
    ResiliencePrioritizeRequest, ResiliencePrioritizeResponse,
    GenerateReportRequest
)
from backend.app.schemas.forest_schemas import (
    ForestCompareRequest, ForestCompareResponse,
    ForestReportGenerateRequest, ForestReportGenerateResponse
)
from backend.app.services.data_service import data_service
from backend.app.services.model_service import model_service
from backend.app.services.resilience_service import resilience_service
from backend.app.services.report_service import report_service
from backend.app.services.india_service import india_service
from backend.app.services.forest_service import forest_service

router = APIRouter()

# 1. Health
@router.get("/health", response_model=HealthResponse)
def get_health():
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "project": settings.PROJECT_NAME,
        "datasets_ready": True,
        "models_ready": True,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

# 2. Data Sources & Provenance
@router.get("/data/sources")
def get_data_sources():
    return data_service.get_data_sources_register()

# 3. Districts List & GeoJSON
@router.get("/districts")
def list_districts():
    return data_service.get_districts()

# 4. District Details
@router.get("/districts/{district_id}")
def get_district_details(district_id: str):
    dist = data_service.get_district_by_id(district_id)
    if not dist:
        raise HTTPException(status_code=404, detail=f"District '{district_id}' not found.")
    return dist

# 5. ENSO History
@router.get("/enso/history")
def get_enso_history():
    return data_service.get_enso_history()

# 6. Current ENSO State
@router.get("/enso/current")
def get_enso_current():
    return data_service.get_current_enso()

# 7. ENSO Historical Events
@router.get("/enso/events")
def get_enso_events():
    return data_service.get_enso_events()

# 8. Rainfall History
@router.get("/rainfall/history")
def get_rainfall_history(district_id: str = Query(None, description="Filter by district ID e.g. WAR")):
    return data_service.get_rainfall_history(district_id)

# 9. Rainfall Anomalies
@router.get("/rainfall/anomalies")
def get_rainfall_anomalies(district_id: str = Query(None, description="Filter by district ID e.g. WAR")):
    return data_service.get_rainfall_anomalies(district_id)

# 10. Satellite Layers (WMS & Rasters)
@router.get("/satellite/layers")
def get_satellite_layers():
    return data_service.get_satellite_layers()

# 11. Satellite Metadata
@router.get("/satellite/metadata")
def get_satellite_metadata():
    return data_service.get_satellite_metadata()

# 12. Vegetation History
@router.get("/vegetation/history")
def get_vegetation_history(district_id: str = Query(None, description="Filter by district ID e.g. WAR")):
    return data_service.get_vegetation_history(district_id)

# 13. Vegetation Anomalies & Zonal Stats
@router.get("/vegetation/anomalies")
def get_vegetation_anomalies(district_id: str = Query(None, description="Filter by district ID e.g. WAR")):
    return data_service.get_vegetation_anomalies(district_id)

# 14. ML Models Registry
@router.get("/models")
def list_models():
    return model_service.get_models_list()

# 15. Model Metrics
@router.get("/models/{model_id}/metrics")
def get_model_metrics(model_id: str):
    metrics = model_service.get_model_metrics(model_id)
    if not metrics:
        raise HTTPException(status_code=404, detail=f"Model '{model_id}' not found.")
    return metrics

# 16. Model Features & SHAP Explainability
@router.get("/models/{model_id}/features")
def get_model_features(model_id: str):
    return model_service.get_model_features(model_id)

# 17. Risk Prediction Inference
@router.post("/risk/predict", response_model=PredictRiskResponse)
def predict_risk(payload: PredictRiskRequest):
    dist = data_service.get_district_by_id(payload.district_id)
    if not dist:
        raise HTTPException(status_code=404, detail=f"District '{payload.district_id}' not found.")
    
    result = model_service.predict_risk(
        district_meta=dist,
        enso_mam=payload.nino34_mam,
        enso_trend=payload.nino34_trend,
        pre_rf=payload.preseason_mam_rainfall_mm,
        pre_ndvi=payload.preseason_may_ndvi,
        model_id=payload.model_id or "model_b_enso_lr"
    )
    return result

# 18. Resilience Prioritization
@router.post("/resilience/prioritize", response_model=ResiliencePrioritizeResponse)
def prioritize_resilience(payload: ResiliencePrioritizeRequest):
    return resilience_service.prioritize_districts(
        risk_weight=payload.risk_weight,
        veg_stress_weight=payload.vegetation_stress_weight,
        exposure_weight=payload.exposure_weight,
        irrigation_weight=payload.irrigation_vulnerability_weight,
        year=payload.year or 2024
    )

# 19. Generate Evidence Report
@router.post("/reports/generate")
def generate_report(payload: GenerateReportRequest):
    try:
        report_meta = report_service.generate_district_report(
            district_id=payload.district_id,
            year=payload.year
        )
        return report_meta
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")

# 20. Download Evidence Report PDF
@router.get("/reports/{report_id}")
def download_report(report_id: str):
    filename = f"{report_id}.pdf" if not report_id.endswith(".pdf") else report_id
    filepath = os.path.join(settings.REPORTS_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Requested report PDF does not exist.")
    return FileResponse(filepath, media_type="application/pdf", filename=filename)

# 21. India States List & GeoJSON
@router.get("/india/states")
def get_india_states():
    return india_service.get_all_states()

# 22. India State Detail
@router.get("/india/states/{state_id}")
def get_india_state(state_id: str):
    res = india_service.get_state_by_id(state_id)
    if not res:
        raise HTTPException(status_code=404, detail=f"State '{state_id}' not found.")
    return res

# 23. India State Districts
@router.get("/india/states/{state_id}/districts")
def get_india_state_districts(state_id: str):
    return india_service.get_districts_for_state(state_id)

# 24. India District Detail
@router.get("/india/districts/{district_id}")
def get_india_district(district_id: str):
    res = india_service.get_district_by_id(district_id)
    if not res:
        raise HTTPException(status_code=404, detail=f"District '{district_id}' not found.")
    return res

# 25. Forest Coverage
@router.get("/forest/coverage")
def get_forest_coverage():
    return forest_service.get_coverage()

# 26. Forest Change & Trajectory
@router.get("/forest/change")
def get_forest_change(region_id: str = Query("NATIONAL", description="Region ID e.g. NATIONAL, AP, TS, WAR, GAD")):
    return forest_service.get_change(region_id)

# 27. Forest Loss History
@router.get("/forest/loss/history")
def get_forest_loss_history(region_id: str = Query("NATIONAL", description="Region ID e.g. NATIONAL, TS, WAR")):
    return forest_service.get_loss_history(region_id)

# 28. Forest Loss Regional Rankings
@router.get("/forest/loss/regions")
def get_forest_loss_regions(
    region_type: str = Query("states", description="states or districts"),
    sort_by: str = Query("loss_2023_ha", description="loss_2023_ha, loss_pct_2023, or total_loss_2001_2023_ha"),
    limit: int = Query(20, ge=1, le=100)
):
    return forest_service.get_loss_regions(region_type, sort_by, limit)

# 29. Forest Satellite Scenes
@router.get("/forest/satellite-scenes")
def get_forest_satellite_scenes():
    return forest_service.get_satellite_scenes()

# 30. Forest Change Map (Choropleth GeoJSON)
@router.get("/forest/change-map")
def get_forest_change_map():
    return forest_service.get_change_map()

# 31. Forest Provenance Registry
@router.get("/forest/provenance")
def get_forest_provenance():
    return forest_service.get_provenance()

# 32. Forest Compare Inference
@router.post("/forest/compare", response_model=ForestCompareResponse)
def compare_forest(payload: ForestCompareRequest):
    return forest_service.compare_forest(
        region_id=payload.region_id,
        baseline_year=payload.baseline_year or 2019,
        recent_year=payload.recent_year or 2023,
        canopy_class=payload.canopy_class or "OF"
    )

# 33. Generate Forest Evidence Report
@router.post("/forest/reports/generate", response_model=ForestReportGenerateResponse)
def generate_forest_report(payload: ForestReportGenerateRequest):
    try:
        return forest_service.generate_report(payload.region_id, payload.region_type or "district")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating forest report: {str(e)}")

