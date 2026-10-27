# VARUNA 2047: Automated Testing & Validation Guide

**Project:** VARUNA 2047 — National Earth Intelligence for Agricultural and Environmental Resilience  
**Competition:** Hack for Social Cause — VBYLD 2027  
**Team:** bulls_eye  

This document details the automated test suite, verification procedures, expected results, and test execution commands across the backend API, geospatial engine, forest-change detection pipeline, and Next.js frontend production bundle.

---

## 1. Test Environment Setup & Prerequisites

### Python Backend Dependencies
Install test and runtime dependencies:
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
pip install pytest httpx
```

### Frontend Dependencies
```bash
cd frontend
npm install
```

---

## 2. Test Execution Commands

### A. Run Full Python Test Suite
```bash
pytest -v
```
To run specific sub-suites:
```bash
# Backend REST API tests (core endpoints)
pytest -v tests/backend/test_api.py

# India Nationwide GIS & ForestWatch API tests
pytest -v tests/backend/test_india_forest_api.py

# Geospatial processing & geometry transformation tests
pytest -v tests/geospatial/test_engine.py

# Sentinel-2 dNDVI change detection & forest classification tests
pytest -v tests/geospatial/test_forest_engine.py
```

### B. Run Live Endpoints Audit (Frontend + Backend)
With the backend running on port 8000 and frontend on port 3000:
```bash
python scripts/audit_live_endpoints.py
```

### C. Run Next.js Production Build Validation
```bash
cd frontend
npm run build
```

---

## 3. Detailed Test Suite Coverage

### 3.1 Backend REST API Suite (`tests/backend/test_api.py`)
- `test_health_endpoint`: Verifies `/api/health` returns status `healthy`, API version `1.0.0`, and dataset readiness.
- `test_data_sources_endpoint`: Verifies `/api/data/sources` reports active data providers (NOAA, NASA, ESA, ISRO, FSI).
- `test_districts_endpoint`: Verifies `/api/districts` returns valid district list with geographic metadata.
- `test_district_detail_valid`: Verifies district detail query for Warangal (`WAR`).
- `test_district_detail_invalid`: Verifies proper `HTTP 404 Not Found` error handling for invalid district IDs.
- `test_enso_endpoints`: Verifies `/api/enso/history`, `/api/enso/current`, and `/api/enso/events` return structured ONI anomaly time-series.
- `test_rainfall_endpoints`: Verifies rainfall history and climatological anomaly endpoints.
- `test_satellite_layers`: Verifies multi-spectral Earth Observation layers (True Color, False Color, NDVI, NDWI).
- `test_models_and_metrics`: Verifies machine learning model registry and performance metrics.
- `test_risk_predict_endpoint`: Verifies drought risk prediction POST endpoint.
- `test_resilience_prioritize_endpoint`: Verifies multi-criteria decision analysis prioritization engine.
- `test_report_generation`: Verifies automated PDF research dossier compilation.

### 3.2 Nationwide India GIS & ForestWatch API (`tests/backend/test_india_forest_api.py`)
- `test_india_states_endpoint`: Verifies `/api/india/states` returns all 36 States and Union Territories.
- `test_india_state_detail`: Verifies state detail resolution for Telangana (`TS`).
- `test_india_state_districts`: Verifies all districts belonging to a specified state are returned.
- `test_india_district_detail`: Verifies district detail queries across nationwide district IDs.
- `test_forest_coverage`: Verifies ISFR baseline coverage percentages.
- `test_forest_change_national`: Verifies national Hansen GFC tree cover loss metrics.
- `test_forest_change_district`: Verifies district-level canopy disturbance metrics.
- `test_forest_loss_history`: Verifies annual loss time-series from 2000 to 2023.
- `test_forest_loss_regions`: Verifies regional loss rankings.
- `test_forest_satellite_scenes`: Verifies Sentinel-2 L2A scene metadata catalog.
- `test_forest_change_map`: Verifies vector disturbance features.
- `test_forest_provenance`: Verifies complete scientific citations and disclosures.
- `test_forest_compare_post`: Verifies satellite before/after comparison POST endpoint.
- `test_forest_report_generate`: Verifies evidence report generation for forest corridors.

### 3.3 Geospatial Processing Engine (`tests/geospatial/test_engine.py`)
- `test_validate_geometry_clean`: Verifies polygon topology validation and self-intersection repair.
- `test_transform_crs`: Verifies spatial coordinate transformation (EPSG:4326 WGS84 $\leftrightarrow$ EPSG:32644 UTM 44N).
- `test_compute_ndvi_values`: Verifies Normalized Difference Vegetation Index computation:
  $$\text{NDVI} = \frac{\text{NIR} - \text{Red}}{\text{NIR} + \text{Red}}$$
  with zero-division protection and $[-1.0, 1.0]$ bounds.
- `test_zonal_stats_synthetic`: Verifies polygon zonal statistics calculation over raster grids.

### 3.4 Sentinel-2 Canopy Change Engine (`tests/geospatial/test_forest_engine.py`)
- `test_canopy_classification`: Verifies canopy density classification (VDF: $>70\%$, MDF: $40\text{--}70\%$, OF: $10\text{--}40\%$, Non-Forest: $<10\%$).
- `test_disturbance_classification`: Verifies delta-NDVI disturbance thresholding:
  - Stable / Regrowth: $\Delta\text{NDVI} > -0.15$
  - Low Canopy Disturbance: $-0.25 < \Delta\text{NDVI} \le -0.15$
  - Moderate Canopy Disturbance: $-0.40 < \Delta\text{NDVI} \le -0.25$
  - High Canopy Disturbance: $\Delta\text{NDVI} \le -0.40$
- `test_change_detection_engine`: Verifies cloud masking and bi-temporal pixel subtraction.
- `test_tree_count_estimation`: Enforces scientific limitation that arbitrary tree multipliers are disabled and only measured hectares are reported.
- `test_zonal_statistics`: Verifies zonal area aggregation.

---

## 4. Actual Verified Test Results

### Pytest Execution Summary
```
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\RACHIKA\HFS
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.14.0
collected 35 items

tests/backend/test_api.py::test_health_endpoint PASSED                   [  2%]
tests/backend/test_api.py::test_data_sources_endpoint PASSED             [  5%]
tests/backend/test_api.py::test_districts_endpoint PASSED                [  8%]
tests/backend/test_api.py::test_district_detail_valid PASSED             [ 11%]
tests/backend/test_api.py::test_district_detail_invalid PASSED           [ 14%]
tests/backend/test_api.py::test_enso_endpoints PASSED                    [ 17%]
tests/backend/test_api.py::test_rainfall_endpoints PASSED                [ 20%]
tests/backend/test_api.py::test_satellite_layers PASSED                  [ 22%]
tests/backend/test_api.py::test_models_and_metrics PASSED                [ 25%]
tests/backend/test_api.py::test_risk_predict_endpoint PASSED             [ 28%]
tests/backend/test_api.py::test_resilience_prioritize_endpoint PASSED    [ 31%]
tests/backend/test_api.py::test_report_generation PASSED                 [ 34%]
tests/backend/test_india_forest_api.py::test_india_states_endpoint PASSED [ 37%]
tests/backend/test_india_forest_api.py::test_india_state_detail PASSED   [ 40%]
tests/backend/test_india_forest_api.py::test_india_state_districts PASSED [ 42%]
tests/backend/test_india_forest_api.py::test_india_district_detail PASSED [ 45%]
tests/backend/test_india_forest_api.py::test_forest_coverage PASSED      [ 48%]
tests/backend/test_india_forest_api.py::test_forest_change_national PASSED [ 51%]
tests/backend/test_india_forest_api.py::test_forest_change_district PASSED [ 54%]
tests/backend/test_india_forest_api.py::test_forest_loss_history PASSED  [ 57%]
tests/backend/test_india_forest_api.py::test_forest_loss_regions PASSED  [ 60%]
tests/backend/test_india_forest_api.py::test_forest_satellite_scenes PASSED [ 62%]
tests/backend/test_india_forest_api.py::test_forest_change_map PASSED    [ 65%]
tests/backend/test_india_forest_api.py::test_forest_provenance PASSED    [ 68%]
tests/backend/test_india_forest_api.py::test_forest_compare_post PASSED  [ 71%]
tests/backend/test_india_forest_api.py::test_forest_report_generate PASSED [ 74%]
tests/geospatial/test_engine.py::test_validate_geometry_clean PASSED     [ 77%]
tests/geospatial/test_engine.py::test_transform_crs PASSED               [ 80%]
tests/geospatial/test_engine.py::test_compute_ndvi_values PASSED         [ 82%]
tests/geospatial/test_engine.py::test_zonal_stats_synthetic PASSED       [ 85%]
tests/geospatial/test_forest_engine.py::test_canopy_classification PASSED [ 88%]
tests/geospatial/test_forest_engine.py::test_disturbance_classification PASSED [ 91%]
tests/geospatial/test_forest_engine.py::test_change_detection_engine PASSED [ 94%]
tests/geospatial/test_forest_engine.py::test_tree_count_estimation PASSED [ 97%]
tests/geospatial/test_forest_engine.py::test_zonal_statistics PASSED     [100%]

======================= 35 passed, 17 warnings in 8.96s =======================
```

### Next.js Production Build Summary
```
> frontend@0.1.0 build
> next build

▲ Next.js 16.4.3 (Turbopack)
✓ Running next.config.ts took 80ms
- Cache Components enabled
- Partial Prefetching enabled

  Creating an optimized production build ...
✓ Compiled successfully in 2.7s
  Running TypeScript ...
  Finished TypeScript in 4.5s ...
✓ Generating static pages using 15 workers (14/14) in 3.7s

Route (app)
┌ ○ /
├ ○ /_not-found
├ ○ /enso
├ ○ /explorer
├ ○ /forestwatch
├ ○ /india
├   /india/[state]/[district]
│ └ ◐ /india/[state]/[district]
├ ○ /reports
├ ○ /research
├ ○ /resilience
├ ○ /risk-lab
└ ○ /vegetation

○  (Static)             prerendered as static content
◐  (Partial Prerender)  prerendered as static HTML with dynamic server-streamed content
```
**Build Status: 100% Success, 0 Errors, 0 Warnings.**

---

## 5. Known Limitations & Test Scope

1. **Regional Model Scope:** Machine learning risk models are strictly validated against Telangana longitudinal historical data (2014–2024). Models are not generalized to distinct agro-ecological zones outside the Deccan plateau.
2. **Sentinel-2 Spatial Boundary:** The high-resolution (10m) change detection slider is validated for Tile `44QLE` (Warangal ecological corridor). Nationwide tree cover loss uses Hansen GFC (30m) aggregates.
3. **Web Worker Headless Limitations:** While the MapLibre Web Worker (`maplibre-gl-worker.mjs`) loads and runs in all standard desktop and mobile browsers, headless environments without WebGL context may require software rendering (`swiftshader` / `mesa`) for canvas snapshot testing.
