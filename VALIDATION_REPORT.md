# VARUNA 2047: Validation & Scientific Verification Report

**Evaluation Timestamp:** October 2026  
**Auditor / Principal Engineer:** Geospatial AI & Climate Verification Engine  
**Execution Environment:** Windows Server / Python 3.12.10 / Node.js v24.16.0  

---

## 1. Automated Test Suite Execution

All automated tests were executed using `pytest` version 9.1.1 across backend API services, ML inference modules, and geospatial algorithms.

### Summary of Executed Tests

```
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\RACHIKA\HFS
configfile: pytest.ini
plugins: anyio-4.14.0
collected 16 items

tests\backend\test_api.py ............                                   [ 75%]
tests\geospatial\test_engine.py ....                                     [100%]

======================= 16 passed, 17 warnings in 5.54s =======================
```

### Detailed Test Results Breakdown

| Test File | Test Case | Target Subsystem | Status | Observed Outcome |
|---|---|---|---|---|
| `test_api.py` | `test_health_endpoint` | Backend Core | **PASS** | HTTP 200, datasets_ready: true, models_ready: true |
| `test_api.py` | `test_data_sources_endpoint` | Provenance API | **PASS** | HTTP 200, 4 core providers verified, ISRO audit present |
| `test_api.py` | `test_districts_endpoint` | Districts Listing | **PASS** | HTTP 200, 6 Telangana pilot districts & GeoJSON verified |
| `test_api.py` | `test_district_detail_valid` | District Detail | **PASS** | HTTP 200, Warangal elevation: 280m, coords verified |
| `test_api.py` | `test_district_detail_invalid` | Error Handling | **PASS** | HTTP 404 cleanly returned on invalid ID |
| `test_api.py` | `test_enso_endpoints` | NOAA Ingestion | **PASS** | HTTP 200, 920 seasonal ONI observations parsed |
| `test_api.py` | `test_rainfall_endpoints` | NASA Precipitation | **PASS** | HTTP 200, 44 years parsed, climatological normals verified |
| `test_api.py` | `test_satellite_layers` | Remote Sensing API | **PASS** | HTTP 200, 4 layers including live ISRO Bhuvan WMS |
| `test_api.py` | `test_models_and_metrics` | ML Registry | **PASS** | HTTP 200, 4 benchmarked models registered |
| `test_api.py` | `test_risk_predict_endpoint` | Risk Inference | **PASS** | HTTP 200, deficit probability within [0, 1] range |
| `test_api.py` | `test_resilience_prioritize_endpoint` | Resilience MCDA | **PASS** | HTTP 200, 6 districts ranked with composite scores |
| `test_api.py` | `test_report_generation` | PDF ReportLab | **PASS** | HTTP 200, PDF binary generated (> 1000 bytes) and streamed |
| `test_engine.py` | `test_validate_geometry_clean` | Vector Engine | **PASS** | Shapely polygon validated and repaired |
| `test_engine.py` | `test_transform_crs` | CRS Transformation | **PASS** | EPSG:4326 to EPSG:3857 projected accurately |
| `test_engine.py` | `test_compute_ndvi_values` | NDVI Computation | **PASS** | Division-by-zero guarded, scientific range [-1, 1] |
| `test_engine.py` | `test_zonal_stats_synthetic` | Raster Zonal Stats | **PASS** | Rasterio polygon masking and zonal mean verified |

---

## 2. Machine Learning Ablation & Out-of-Sample Performance

### Primary Evaluation: Untouched Held-Out Test Set (2019–2024: 36 District-Years)

> **CRITICAL SCIENTIFIC INTEGRITY AUDIT FINDING:**  
> On the untouched 2019–2024 held-out test period, **the Climatological Base Rate model decisively outperforms all Machine Learning models** on Brier Score (0.0408 vs 0.1698–0.2182) and Log Loss (0.2257 vs 0.5192–0.6264).

| Model Architecture | Features Used | Brier Score (lower is better) | Log Loss | ROC-AUC | F1-Score | False Alarms ($p \ge 0.5$) |
|---|---|---|---|---|---|---|
| **Climatological Base Rate (Best)** | Historical Training Mean ($p=0.202$) | **0.0408** | **0.2257** | Undefined ($N_+=0$) | 0.0000 | 0 / 36 |
| **ENSO-Only Logistic Regression** | Niño 3.4 DJF, MAM, Trend, Phase | 0.2182 | 0.6264 | Undefined ($N_+=0$) | 0.0000 | 12 / 36 |
| **ENSO + Climate Logistic Regression** | ENSO + Pre-monsoon MAM rain + Lag | 0.1698 | 0.5192 | Undefined ($N_+=0$) | 0.0000 | 9 / 36 |
| **VARUNA Multimodal XGBoost** | Full Multimodal (16 features) | 0.1913 | 0.5308 | Undefined ($N_+=0$) | 0.0000 | 14 / 36 |

### Scientific Root Cause Analysis
1. **Absence of Drought in Test Set (Target Quiescence):** 2019 through 2024 experienced 6 consecutive wet-to-normal monsoon seasons across Telangana (anomalies: +2.5% to +54.3%). Zero positive deficit events ($y=1$) occurred ($N_+=0, N_-=36$). Because $y_{\text{true}}$ contains only class 0, **ROC-AUC is mathematically undefined** on the untouched test set.
2. **False Alarms and Quadratic Penalty:** During 2019 (weak El Niño) and 2023 (strong El Niño, ONI $+2.0^\circ\text{C}$), the ML models elevated drought probabilities to $0.45–0.70$. Because local droughts were mitigated by a positive Indian Ocean Dipole and late-season Bay of Bengal depressions, no drought occurred in Telangana, resulting in 9–14 false alarms and heavy Brier score penalties.
3. **Climatology Superiority under Normal/Wet Regimes:** Climatology predicted the historical base rate ($p=0.202$) for every case, yielding $(0.202 - 0)^2 = 0.0408$. In the absence of rare hazards, a conservative climatological prior decisively beats complex dynamic models.

---

### Secondary Evaluation: Post-Hoc Multi-Regime Exploration (2015–2024: 60 District-Years)
*Note: This window combines the validation period (which captured the severe 2015 El Niño drought) with the test period to inspect behavior across contrasting drought (2015) and wet (2020) regimes. It is an exploratory post-hoc diagnostic, NOT a pure held-out test metric.*

| Model Architecture | Features Used | Brier Score | ROC-AUC | F1-Score | Diagnostic Behavior |
|---|---|---|---|---|---|
| Climatological Base Rate | Historical Mean ($p=0.202$) | 0.1103 | Undefined | 0.0000 | Uninformative baseline |
| ENSO-Only Logistic Regression | Niño 3.4 DJF, MAM, Trend, Phase | 0.2158 | **0.7830** | **0.3784** | Captures 2015 drought; false alarms in 2023 |
| ENSO + Climate Logistic Regression | ENSO + Pre-monsoon MAM rain | 0.1945 | 0.6388 | 0.0741 | Regularized |
| VARUNA Multimodal XGBoost | Full Multimodal Stack | 0.1881 | 0.4960 | 0.0000 | Decision tree conservatism |

---

## 3. Frontend Production Build Verification

The Next.js 16 frontend application was built using Turbopack:
```
▲ Next.js 16.4.3 (Turbopack)
✓ Compiled successfully in 18.2s
  Running TypeScript ...
  Finished TypeScript in 4.9s ...
✓ Generating static pages using 12 workers (11/11) in 1378ms

Route (app)
┌ ○ / (Mission Control)
├ ○ /_not-found
├ ○ /enso (ENSO Observatory)
├ ○ /explorer (Earth Observation Explorer)
├ ○ /reports (Evidence Reports)
├ ○ /research (Research & Transparency)
├ ○ /resilience (Resilience Planner)
├ ○ /risk-lab (AI Risk Laboratory)
└ ○ /vegetation (Agricultural Stress Explorer)

○ (Static) prerendered as static content
```
Status: **100% Production Build Clean.** Zero runtime warnings.

---

## 4. ISRO Integration & Satellite Provenance Audit

- **Verified ISRO Thematic & Administrative Services:**
  - `sisdpv2:TS_Warangal_lulc_v2`: ISRO NRSC Space Based Information Support for Decentralised Planning (SISDP-2) 1:50,000 Land Use / Land Cover (HTTP 200, verified PNG).
  - `gw:TELANGANA_PRE`: ISRO NRSC Rajiv Gandhi National Drinking Water Mission (RGNDWM) Ground Water Prospects (Pre-Monsoon) (HTTP 200, verified PNG).
  - `bhuvan:telangana_district_boundary`: ISRO NRSC Telangana District Administrative Cartography (HTTP 200).
- **Documented Bhoonidhi SSO Limitation:** Raw multi-spectral raster scene downloads from ISRO Bhoonidhi mandate interactive SSO session cookies and CAPTCHA tokens, preventing programmatic headless ingestion in an open, credential-free repository.
- **Satellite Raster Provenance Disclosure:**
  - The four local GeoTIFF rasters in `data/processed/satellite/` (`ndvi_premonsoon_may.tif`, `ndvi_monsoon_peak.tif`, `ndvi_monsoon_drought_scenario.tif`, `ndvi_anomaly_map.tif`) were generated via mathematical biophysical modeling functions for Deccan agro-ecological conditions to demonstrate Rasterio georeferencing, polygon zonal statistics, and UI rendering.
  - They are transparently labeled as **`[SIMULATION]`** grids and are NOT described as direct observational satellite scenes.
  - Multi-decadal historical NDVI series (1982–2024) is a precipitation-driven simulation proxy, acknowledging that operational Sentinel-2 launched in 2015 and MODIS in 1999.
