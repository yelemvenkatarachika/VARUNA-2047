# VARUNA 2047: National Earth Intelligence for Agricultural and Environmental Resilience

> **Tagline:** *From Global Climate Signals to Local Agricultural Resilience*  
> **Event:** Hack for Social Cause (HSC) — VBYLD 2027  
> **Team:** bulls_eye  
> **Primary Theme:** AI, GIS & Emerging Technologies  
> **Secondary Themes:** Environment & Sustainability • Rural Development & Livelihoods  
> **UN Sustainable Development Goals:** SDG 2 (Zero Hunger) • SDG 13 (Climate Action) • SDG 15 (Life on Land) • SDG 6 (Clean Water)  

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-16.4.3-black.svg)](https://nextjs.org/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-v4-38B2AC.svg)](https://tailwindcss.com/)
[![MapLibre](https://img.shields.io/badge/MapLibre_GL-v6.16-blueviolet.svg)](https://maplibre.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg)](LICENSE)
[![Tests: Pytest](https://img.shields.io/badge/Pytest-35%20Passed-brightgreen.svg)](docs/TESTING.md)

---

## 1. Project Overview & The Social Problem

Indian agriculture supports over **140 million farm households**, with **85% categorized as smallholder or marginal farmers**. Over **52% of India's net sown area is purely rainfed**, leaving rural livelihoods acutely vulnerable to erratic Southwest Monsoon onsets, mid-season dry spells, and climate-induced meteorological droughts.

Simultaneously, accelerated canopy loss and microclimatic degradation in forest corridors reduce moisture retention, heighten topsoil erosion, and compromise watershed hydrology.

### The Problem in Practice
Critical Earth Observation (EO) data exists in disjointed institutional silos:
- Global sea-surface temperature indices (**NOAA CPC ENSO**) remain disconnected from local district forecasting.
- Surface solar radiation and climatological rainfall reanalysis (**NASA POWER**) lack automated integration with state cadastral maps.
- Nationwide administrative forest baselines (**FSI ISFR**) are published in static biennial reports without real-time high-resolution satellite validation.
- District agricultural planners lack an **explainable, multi-tier decision-support system** to identify pre-monsoon risk signals and prioritize watershed interventions.

### The VARUNA 2047 Solution
**VARUNA 2047** bridges this divide by providing an end-to-end, scientifically defensible Earth Intelligence platform. It pairs nationwide administrative GIS mapping across all **36 States/UTs and 734 Districts** with genuine **10-meter Copernicus Sentinel-2 MSI** satellite change detection, **74 years of NOAA ENSO teleconnections**, and **interpretable XGBoost machine learning risk models** to protect rural livelihoods and ecological corridors.

---

## 2. Competition Alignment

- **Primary Theme:** **AI, GIS & Emerging Technologies**
  - WebGL vector map engine (MapLibre GL JS v6) powered by an isolated Web Worker.
  - Multi-spectral Level-2A Bottom-Of-Atmosphere (BOA) satellite pixel analysis (Sentinel-2 10m).
  - Machine learning models (XGBoost, Random Forest, Logistic Regression) with TreeSHAP feature attributions.
- **Secondary Theme 1:** **Environment & Sustainability**
  - Nationwide ForestWatch module tracking Hansen Global Forest Change (30m) tree cover loss (2000–2023) across all 36 States/UTs.
  - Candidate canopy disturbance detection across ecological reserves (Pakhal corridor, Warangal).
- **Secondary Theme 2:** **Rural Development & Livelihoods**
  - District Agricultural Resilience Planner prioritizing irrigation support, watershed harvesting, and contingency crop planning.
  - Automated generation of downloadable PDF evidence dossiers for local agricultural extension officers.

---

## 3. Project Objectives

1. **Nationwide Administrative GIS Centerpiece:** Build an interactive vector map visualizing all 28 States, 8 Union Territories, and 734 Districts with real Survey of India (SOI) geometries, validated interior labels, and dynamic layer styling.
2. **Authentic Satellite Earth Observation:** Implement genuine bi-temporal satellite change detection using Copernicus Sentinel-2 Level-2A Cloud-Optimized GeoTIFFs (COGs), replacing synthetic textures with real pixel-level spectral analysis.
3. **Global-to-Local Climate Teleconnections:** Synthesize 74 years of NOAA Oceanic Niño Index (ONI) records to analyze Pacific Walker circulation anomalies and their historical impact on Indian Summer Monsoon Rainfall (ISMR).
4. **Explainable Multimodal Risk Modeling:** Train and evaluate machine learning models (with zero target leakage and strict pre-monsoon May 31 cutoffs) on longitudinal district ground truth to predict agricultural drought stress.
5. **Decoupled, Production-Ready Architecture:** Deliver an open-source, reproducible stack featuring a FastAPI REST API and a Next.js 16 (Turbopack) frontend with clean test suites and zero mandatory paid API keys.

---

## 4. Key Implemented Features

| Module / Page | Route | Description |
| :--- | :--- | :--- |
| **Mission Control Dashboard** | `/` | Central telemetry displaying active NOAA ONI phase, nationwide forest cover baseline (21.71%), live data hub status, and direct module shortcuts. |
| **Nationwide India GIS Map** | `/india` | 72%/28% GIS dashboard layout. MapLibre GL JS vector map of all 36 States/UTs and 734 Districts with state search, layer switcher (Admin, ForestWatch loss, FSI canopy %, Monsoon rain), and regional intelligence panel. |
| **Regional District Workspace** | `/india/[state]/[district]` | Deep-dive district profile (e.g. Warangal, Telangana) with agro-ecological attributes, climatological rainfall normal, candidate vegetation disturbance metrics, and one-click PDF dossier export. |
| **ForestWatch & Satellite Slider** | `/forestwatch` | State-level Hansen GFC (30m) loss rankings (2000–2023) and split-screen satellite comparison slider evaluating genuine Sentinel-2 2019 vs 2024 Level-2A imagery for Tile `44QLE`. |
| **ENSO Climate Observatory** | `/enso` | Interactive 74-year Oceanic Niño Index time series (1950–2024), El Niño / La Niña episode filtering, and correlation analysis against Indian monsoon anomalies. |
| **Earth Observation Explorer** | `/explorer` | Multi-spectral band combination visualizer (True Color, False Color Infrared, Agriculture, Water) with ISRO Bhuvan WMS thematic overlays. |
| **AI Risk Laboratory** | `/risk-lab` | Comparative model evaluation benchmarks (Logistic Regression, Random Forest, XGBoost), out-of-sample Brier scores, and global TreeSHAP feature attributions. |
| **Vegetation Stress Tracker** | `/vegetation` | Seasonal vegetative drought tracking using NDVI/VCI anomalies and climatological dry-season baselines. |
| **District Resilience Planner** | `/resilience` | Multi-Criteria Decision Analysis (MCDA) tool allowing policy makers to adjust weights for drought risk, vegetative stress, crop exposure, and irrigation deficit. |
| **Automated Evidence Reports** | `/reports` | One-click compilation of research-grade PDF dossiers powered by ReportLab containing full sensor provenance, charts, and policy recommendations. |
| **Scientific Provenance Register** | `/research` | Public catalog of all data sources, citations, spatial resolutions, acquisition parameters, and methodological limitation disclosures. |

---

## 5. UI & Architecture Previews

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  VARUNA 2047 | National Earth Intelligence                  [Data Hub: Verified Active 🟢]             │
├──────────────────────────────────────────────────────────────────┬─────────────────────────────────────┤
│  INDIA GIS MAP (MapLibre WebGL - 72% Width)                      │  REGIONAL INTELLIGENCE (28% Width)  │
│                                                                  │                                     │
│  [Search: 36 States / 734 Districts...] [Layers: Admin|FW|FSI]  │  TELANGANA                          │
│                                                                  │  Area: 1,12,077 sq km               │
│         ▲                                                        │  FSI Baseline: 18.93% (21,214 km²)  │
│       /   \        (Crisp Cyan-Teal State Borders)               │  Districts Mapped: 33               │
│      / TS  \ ◄── Selected State Highlight (Turquoise #0d9488)    │  ─────────────────────────────────  │
│     /       \                                                    │  DISTRICT: WARANGAL                 │
│    └─────────┘     (Zoom ≥ 5.5: 734 District Outlines Rendered)  │  Area: 2,175 sq km                  │
│                                                                  │  Normal Rain: 890 mm                │
│  [Legend: Muted Navy Fill | Cyan Outline | High-Contrast Halos]  │  Candidate Disturbance: 236.2 ha    │
│                                                                  │  [Open Regional Workspace ➔]        │
└──────────────────────────────────────────────────────────────────┴─────────────────────────────────────┘
```

Detailed visual verification records and workflows are available in [docs/DEMO_GUIDE.md](docs/DEMO_GUIDE.md).

---

## 6. Technical Architecture

VARUNA 2047 utilizes a decoupled microservice and client architecture:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        DATA SOURCES & INGESTION                        │
│  ESA Sentinel-2 (10m BOA) • NOAA ONI • NASA POWER • SOI / RGI • FSI    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Automated ETL Scripts
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        GEOSPATIAL & ML STORAGE                         │
│  • GeoJSON: 36 States (58 KB) + 734 Districts (6.26 MB)               │
│  • Sentinel-2 L2A BOA Crops & dNDVI Masks (Pakhal Corridor)            │
│  • Multimodal Feature Matrices (2014-2024 Longitudinal Ground Truth)   │
│  • Serialized XGBoost & Random Forest Models (.pkl)                    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   FASTAPI BACKEND SERVICE (PORT 8000)                  │
│  • /api/india/*: Nationwide state & district spatial queries           │
│  • /api/forest/*: Hansen loss series & Sentinel-2 scene catalog        │
│  • /api/enso/*: 74-year monthly ONI climate time series                │
│  • /api/risk/*: XGBoost multimodal inference & SHAP attributions       │
│  • /api/reports/*: ReportLab dynamic PDF dossier compilation           │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ REST / JSON (CORS Managed)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   NEXT.JS 16 CLIENT (PORT 3000)                        │
│  • MapLibre GL JS v6 with Same-Origin Web Worker (60 FPS WebGL)        │
│  • Minimal 64px Single-Row Navbar with Responsive Mobile Drawer        │
│  • Interactive Sentinel-2 Satellite Comparison Slider                  │
│  • Multi-Criteria Decision Analysis (MCDA) Resilience Planner          │
└────────────────────────────────────────────────────────────────────────┘
```

For complete technical specifications, see [docs/architecture/TECHNICAL_DESIGN_DOCUMENT.md](docs/architecture/TECHNICAL_DESIGN_DOCUMENT.md).

---

## 7. Technology Stack

### Frontend Client
- **Framework:** Next.js 16.4.3 (Turbopack, App Router) with React 19.3.0
- **Language:** TypeScript (Strict mode enabled)
- **Styling:** Tailwind CSS v4 design system
- **Geospatial Mapping:** MapLibre GL JS v6.16.0 with dedicated same-origin Web Worker
- **Vector Glyphs:** Local PBF font glyphs (`Open Sans`, `Arial Unicode MS`)
- **Visualizations:** Recharts 3.10 & Lucide React Iconography

### Backend Service
- **Framework:** FastAPI 0.115+ with ASGI server Uvicorn 0.30+
- **Validation:** Pydantic v2 & Pydantic-Settings
- **HTTP Client:** HTTPX 0.27+ (async requests)
- **Reporting Engine:** ReportLab 4.2+ (PDF generation)

### Geospatial & Earth Observation
- **Raster Processing:** Rasterio 1.3+ & GDAL bindings
- **Vector Processing:** Shapely 2.0+ & GeoPandas 1.0+
- **Coordinate Systems:** PyProj 3.6+ (EPSG:4326 WGS84 $\leftrightarrow$ EPSG:32644 UTM 44N)
- **Data Protocols:** SpatioTemporal Asset Catalog (STAC) & Cloud-Optimized GeoTIFF (COG)

### Machine Learning & Data Science
- **Core ML:** Scikit-Learn 1.4+, XGBoost 2.0+
- **Explainability:** SHAP 0.45+ (TreeSHAP)
- **Data Manipulation:** Pandas 2.2+, NumPy 1.26+
- **Model Serialization:** Joblib 1.4+

---

## 8. Prerequisites

Ensure the following runtimes are installed on your system:
- **Python:** 3.10, 3.11, or 3.12 (Python 3.12 recommended)
- **Node.js:** v18.x, v20.x, or v22.x LTS (Node 20+ recommended)
- **Package Managers:** `pip` (Python) and `npm` (Node)
- **Version Control:** `git`

---

## 9. Complete Installation Steps

### Step 1: Clone Repository
```bash
git clone https://github.com/yelemvenkatarachika/VARUNA-2047.git
cd varuna-2047
```

### Step 2: Python Backend Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# On Linux / macOS:
source venv/bin/activate

# Install all backend dependencies
pip install -r requirements.txt
```

### Step 3: Frontend Client Setup
```bash
cd frontend
npm install
cd ..
```

---

## 10. Environment Variables

Copy the provided environment template to `.env`:
```bash
cp .env.example .env
```

### Variable Reference

| Variable Name | Default Value | Description |
| :--- | :--- | :--- |
| `PROJECT_NAME` | `"VARUNA 2047"` | Application title. |
| `API_HOST` | `"0.0.0.0"` | Backend bind address. |
| `API_PORT` | `8000` | FastAPI server port. |
| `CORS_ORIGINS` | `"http://localhost:3000,http://127.0.0.1:3000"` | Allowed client domains. |
| `NOAA_ONI_URL` | Open NOAA CPC URL | Oceanic Niño Index monthly ASCII feed. |
| `NASA_POWER_BASE` | Open NASA POWER URL | Monthly agrometeorology point API. |
| `NEXT_PUBLIC_API_URL` | `"http://127.0.0.1:8000/api"` | Backend base URL for Next.js client. |

> **Zero Paid Keys Required:** All default features use free, open public endpoints (Esri Dark Canvas basemap, AWS S3 Sentinel-2 COGs, NOAA CPC, NASA POWER).

---

## 11. Data Ingestion & Satellite Processing

All processed data files are pre-bundled in `data/processed/`. To re-run or inspect the automated ingestion pipelines:

```bash
# Ingest authentic NOAA CPC Oceanic Nino Index (1950-2024)
python scripts/ingest_enso.py

# Ingest NASA POWER precipitation and calculate IMD normals
python scripts/ingest_rainfall.py

# Download genuine Sentinel-2 L2A BOA bands, compute dNDVI, and export true-color crops
python scripts/process_satellite_change.py

# Ingest and validate all 36 States and 734 Districts from SOI GeoJSON
python scripts/ingest_complete_india_districts.py

# Generate validated interior state representative label points
python scripts/build_state_labels.py
```

---

## 12. Model Training & Evaluation

To re-train the machine learning models and generate out-of-sample benchmarks:

```bash
# Build the leak-free multimodal training matrix (pre-monsoon May 31 cutoff)
python scripts/build_features.py

# Train Logistic Regression, Random Forest, and XGBoost models
python scripts/train_models.py

# Run out-of-sample evaluation and TreeSHAP feature importance analysis
python scripts/evaluate_models.py
```

Trained models are saved to `models/saved/`:
- `model_b_enso_lr.pkl` (ENSO Logistic Regression)
- `model_c_rf_features.pkl` (Random Forest)
- `model_d_xgboost_multimodal.pkl` (Multimodal XGBoost)

---

## 13. Running the Application

### Start Backend API Server
```bash
# In project root with venv activated:
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```
- API Base: `http://127.0.0.1:8000`
- Interactive Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc Documentation: `http://127.0.0.1:8000/redoc`

### Start Next.js Frontend
```bash
# In another terminal:
cd frontend
npm run dev
```
- Open your browser at: `http://localhost:3000`

---

## 14. Running Automated Tests & Validation

VARUNA 2047 includes automated pytest coverage across the backend API, geospatial engine, and satellite processing pipeline.

```bash
# Run full pytest test suite
pytest -v
```
**Verified Result:** **`35 passed in 8.96s`**

```bash
# Run live backend and frontend endpoint audit
python scripts/audit_live_endpoints.py
```
**Verified Result:** **`All 32 backend endpoints & 11 frontend pages return HTTP 200 OK`**

```bash
# Validate Next.js production build
cd frontend
npm run build
```
**Verified Result:** **`14 of 14 static routes compiled successfully with 0 errors`**

For complete test logs, see [docs/TESTING.md](docs/TESTING.md).

---

## 15. Sample Datasets

Lightweight sample datasets demonstrating all data schemas without distributing multi-gigabyte raw files are located in `data/sample/`:
- [`sample_states.geojson`](data/sample/sample_states.geojson) (State GeoJSON format)
- [`sample_districts.geojson`](data/sample/sample_districts.geojson) (District GeoJSON format)
- [`sample_enso_history.json`](data/sample/sample_enso_history.json) (12-month ONI anomaly records)
- [`sample_rainfall_history.json`](data/sample/sample_rainfall_history.json) (Warangal rainfall series)
- [`sample_forest_loss_response.json`](data/sample/sample_forest_loss_response.json) (Hansen GFC loss structure)
- [`sample_satellite_scenes.json`](data/sample/sample_satellite_scenes.json) (Sentinel-2 scene metadata)
- [`sample_model_features.csv`](data/sample/sample_model_features.csv) (10-feature multimodal input rows)

See [`data/sample/README.md`](data/sample/README.md) for schema specifications.

---

## 16. Data Sources & Attributions

| Provider | Dataset | Terms of Use / License |
| :--- | :--- | :--- |
| **ESA Copernicus** | Sentinel-2 MSI Multi-Spectral Level-2A | [Copernicus Open Access Policy](https://sentinels.copernicus.eu/) (Free public access) |
| **NOAA CPC** | Oceanic Niño Index (ONI, ERSST.v5) | U.S. Public Domain / Open Data |
| **NASA POWER** | Agroclimatology Meteorology | NASA Open Data Policy (Public Domain) |
| **Hansen / UMD / Google** | Global Forest Change v1.11 (30m) | Creative Commons Attribution 4.0 International (CC BY 4.0) |
| **Survey of India (SOI)** | India Administrative Boundaries | Open Government Data (OGD) / NDSAP |
| **Forest Survey of India (FSI)** | ISFR 2021 State Baselines | Published Official Statistics, MoEFCC |
| **Esri** | World Dark Gray Canvas Basemap | ArcGIS Online Public Map Services |

See [docs/DATA_LICENSES.md](docs/DATA_LICENSES.md) for full licensing terms.

---

## 17. Scientific Disclosures & Limitations

1. **Observational Vegetation Disturbance:** The reported **236.21 hectares** of canopy disturbance in the Warangal corridor is strictly classified as **candidate vegetation disturbance detected from bi-temporal Sentinel-2 NDVI change**. Spectral pixel changes can stem from selective thinning, road widening, canopy seasonal senescence, or agricultural boundary shifts. It is **not** asserted as confirmed illegal deforestation or individual tree felling.
2. **Regional ML Modeling Scope:** The multimodal machine learning drought models were trained exclusively on longitudinal historical records (2014–2024) across Telangana districts. Because agricultural drought teleconnections vary across agro-ecological zones, these models are **not** asserted as universal predictors for climatically distinct regions (e.g. Himalayan foothills or Western Ghats).
3. **Pre-Monsoon May 31 Cutoff:** All models strictly utilize observational indicators available on or before May 31 of each forecast year to prevent target leakage.

---

## 18. Evaluator Demo Walkthrough

Judges and evaluators can follow the 10-step guided tour detailed in [docs/DEMO_GUIDE.md](docs/DEMO_GUIDE.md):
1. **Overview (`/`):** Confirm live data hub status and national forest statistics.
2. **India GIS Map (`/india`):** Inspect WebGL rendering of 36 States/UTs with clear boundaries and names.
3. **Select Telangana:** Observe fluid `fitBounds` zoom, state metrics, and district boundary outlines.
4. **Select Warangal:** Inspect district attributes, normal rainfall, and candidate disturbance.
5. **Open Regional Workspace (`/india/ts/war`):** Examine local ecological indicators.
6. **Navigate to ForestWatch (`/forestwatch`):** Review national Hansen loss rankings (2000–2023).
7. **Sentinel-2 Satellite Slider:** Compare genuine 2019 vs 2024 Level-2A imagery for Tile `44QLE`.
8. **Inspect Disturbance Mask:** Toggle the amber dNDVI loss overlay ($236.21\text{ ha}$ disturbance).
9. **Generate Evidence Dossier:** Export an automated research-grade PDF report.
10. **Climate & Risk Lab (`/enso` & `/risk-lab`):** Inspect Pacific ONI teleconnections and TreeSHAP attributions.

---

## 19. Team Contributions

**Team Name:** bulls_eye  
**Competition:** Hack for Social Cause (HSC) — VBYLD 2027  
**Institution / Track:** National Earth Intelligence, AI, GIS & Rural Resilience  

- **Geospatial & Satellite Pipeline:** Integration of Copernicus Sentinel-2 STAC/COG pipelines, bi-temporal dNDVI calculations, and Survey of India vector boundary optimization.
- **Backend Architecture:** FastAPI microservice, Pydantic data schemas, ReportLab PDF generation, and automated live audit test suites.
- **Frontend & WebGL Engineering:** Next.js 16 (Turbopack) application, MapLibre GL Web Worker same-origin deployment, responsive 64px navbar, and interactive satellite split slider.
- **Machine Learning & Climate Teleconnections:** NOAA ONI historical processing, NASA POWER ingestion, leak-free feature matrix assembly, and TreeSHAP explainable risk modeling.

---

## 20. License

Original code and algorithms created by Team bulls_eye are licensed under the **[MIT License](LICENSE)**.  
External datasets and satellite imagery are governed by their respective open access licenses as detailed in [docs/DATA_LICENSES.md](docs/DATA_LICENSES.md).
