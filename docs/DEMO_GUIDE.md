# VARUNA 2047: Evaluator Demo & Presentation Guide

**Competition:** Hack for Social Cause — VBYLD 2027  
**Team:** bulls_eye  
**Project:** VARUNA 2047 — National Earth Intelligence for Agricultural and Environmental Resilience  
**Live Access:** Frontend: `http://localhost:3000` | Backend API Docs: `http://127.0.0.1:8000/docs`  

---

## Quick-Start Startup (2 Commands)

### 1. Terminal 1 — Start FastAPI Backend
```bash
# In project root:
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```
*Expected: Uvicorn running on `http://0.0.0.0:8000` with Swagger docs at `http://127.0.0.1:8000/docs`.*

### 2. Terminal 2 — Start Next.js Frontend
```bash
cd frontend
npm run dev
```
*Expected: Next.js dev server running on `http://localhost:3000`.*

---

## 10-Step Interactive Demo Workflow

This 10-step walkthrough demonstrates the end-to-end integration of global climate teleconnections, national administrative GIS mapping, high-resolution satellite Earth observation, and explainable AI risk intelligence.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 VARUNA 2047 WORKFLOW                                    │
│                                                                                        │
│ [1] Overview ──► [2] India GIS Map ──► [3] Select Telangana ──► [4] Select Warangal   │
│                                                                             │          │
│ [8] Candidate Disturbance ◄── [7] 2019 vs 2024 Sentinel-2 ◄── [6] ForestWatch ◄───┘   │
│          │                                                                             │
│          └──► [9] Generate PDF Evidence Report ──► [10] ENSO & Climate Resilience     │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### Step 1: Open VARUNA 2047 & Inspect the Platform Overview
- **Action:** Open `http://localhost:3000` in Google Chrome or Microsoft Edge.
- **Visuals to Observe:**
  - Modern, dark slate navy (`#020617`) theme with vibrant teal accents.
  - Minimal 64px navbar displaying **VARUNA 2047: National Earth Intelligence**.
  - Top-level Data Hub Status badge showing: `Data Hub: Verified Active` (with a pulsing green dot confirming live connection to FastAPI `/api/health`).
  - Key hero statistics:
    - National Forest Baseline: `21.71%` (7,13,789 sq km).
    - Monitored Administrative Coverage: `36 States/UTs` & `734 Districts`.
    - Satellite Resolution: `10m / 30m` (Copernicus Sentinel-2 & Landsat).

---

### Step 2: Navigate to the Nationwide India GIS Map
- **Action:** Click **India Map** in the top navigation bar (or navigate to `/india`).
- **Visuals to Observe:**
  - The centerpiece 72% / 28% GIS dashboard layout mounts seamlessly.
  - MapLibre GL JS initializes using the local same-origin Web Worker (`/maplibre/maplibre-gl-worker.mjs`) with zero console errors.
  - All 28 States and 8 Union Territories are rendered with visible cyan-teal boundaries (`#14b8a6`) and muted teal fills (`#0f2b33`).
  - State name labels are clearly displayed over interior representative points (e.g., *Telangana*, *Maharashtra*, *Karnataka*, *Rajasthan*, *Odisha*) with dynamic collision avoidance and halo contrast.
  - Layer tabs at top-right allow switching between:
    1. *Administrative View*
    2. *ForestWatch Loss (Hansen GFC)*
    3. *FSI Canopy %*
    4. *Monsoon Rain (IMD Normal mm)*

---

### Step 3: Select Telangana State
- **Action:** Hover over and click on **Telangana** on the vector map (or type "Telangana" into the search bar).
- **Visuals to Observe:**
  - The map smoothly executes a fluid `fitBounds` animation zooming directly into Telangana's bounding box.
  - Telangana's polygon lights up with a rich turquoise fill (`#0d9488`) and bright cyan border (`#5eead4`).
  - The right-hand Regional Intelligence panel updates to **State Administration Mode**:
    - State Area: `1,12,077 sq km`.
    - FSI Forest Baseline: `18.93%` (21,214 sq km).
    - 2023 Annual Loss: `8,420 ha`.
    - Districts Mapped: `33 Districts`.
  - District boundaries for all 33 Telangana districts emerge on the map with thin sky-blue dashed lines (`#38bdf8`).

---

### Step 4: Select Warangal District
- **Action:** In the right panel's district list, click **Warangal** (or search "Warangal" in the autocomplete bar).
- **Visuals to Observe:**
  - The map executes a smooth `flyTo` animation centering at $[79.59^\circ\text{E}, 17.96^\circ\text{N}]$ at zoom level `8.5`.
  - Warangal district boundary is highlighted with an amber selection stroke (`#fbbf24`).
  - Nearby monitored ecological corridors (Pakhal Wildlife Sanctuary corridor) become prominent.

---

### Step 5: Inspect Regional Intelligence for Warangal
- **Action:** Examine the updated right panel in **District Profile Mode**.
- **Metrics Displayed:**
  - Geographical Area: `2,175 sq km`.
  - Forest Baseline: `15.8%`.
  - Candidate Vegetation Disturbance: `236.2 ha`.
  - Monsoon Normal Rainfall: `890 mm`.
  - **Scientific Disclosure Notice:** Prominently highlights that figures reflect *candidate vegetation disturbance detected from NDVI change*, maintaining strict scientific integrity.

---

### Step 6: Open the ForestWatch Earth Observation Module
- **Action:** Click the button **Open Regional Workspace** (or click **ForestWatch** in the navbar).
- **Visuals to Observe:**
  - Navigates to `/forestwatch`.
  - Presents nationwide state loss rankings (Hansen Global Forest Change v1.11).
  - Shows top loss states: Odisha, Assam, Chhattisgarh, Telangana, Madhya Pradesh.
  - Displays annual temporal trends from 2000 through 2023.

---

### Step 7: Compare Genuine 2019 and 2024 Sentinel-2 Observations
- **Action:** Scroll to the **Satellite Evidence Comparison** section for Tile `44QLE` (Warangal Corridor).
- **Visuals to Observe:**
  - Interactive split-screen slider comparing:
    - **Baseline Acquisition:** 2019-01-29 (Sentinel-2B, Level-2A BOA, Sun Elevation: 45.2°).
    - **Recent Acquisition:** 2024-02-18 (Sentinel-2A, Level-2A BOA, Sun Elevation: 46.8°).
  - Imagery displays genuine 10-meter resolution True Color (Bands 4-3-2) crops from the Pakhal reserve forest corridor.
  - Zero procedural fractal noise or synthetic textures are used.

---

### Step 8: Inspect Candidate Vegetation Disturbance
- **Action:** Toggle the **Canopy Disturbance Overlay** button above the satellite slider.
- **Visuals to Observe:**
  - A semi-transparent amber/red mask renders directly over pixels where bi-temporal $\Delta\text{NDVI} < -0.15$.
  - Clear spatial clusters of canopy loss appear along road corridors and fringe agricultural expansions.
  - The calculation box confirms:
    - Analyzed Window: $600 \times 600\text{ pixels}$ ($3{,}600\text{ ha}$).
    - Disturbed Pixels: $23{,}621\text{ pixels} \times 100\text{ m}^2 = 236.21\text{ hectares}$.
    - Reduction in Baseline Canopy: $20.41\%$.

---

### Step 9: Generate an Evidence Report (PDF Research Dossier)
- **Action:** Click **Evidence Reports** in the navbar (or click "Generate Dossier" in the district workspace).
- **Visuals to Observe:**
  - The backend calls ReportLab (`/api/reports/generate` or `/api/forest/reports/generate`).
  - A formatted scientific dossier compiles instantly with:
    - District administrative identification.
    - Climatological normals and monsoon rainfall anomaly history.
    - Sentinel-2 sensor provenance and dNDVI metrics.
    - Recommended agro-forestry and irrigation interventions.
  - Can be downloaded or viewed directly in the browser.

---

### Step 10: Explain ENSO Teleconnections & Climate Resilience
- **Action:** Click **Climate** in the navbar (`/enso`).
- **Visuals to Observe:**
  - Monthly time-series chart of the NOAA Oceanic Niño Index (ONI) from 1950 to 2024.
  - Historical correlation analysis demonstrating how strong El Niño events (e.g., 2002, 2009, 2015) consistently coincide with summer monsoon deficits across central and southern India.
  - Under **More $\rightarrow$ AI Risk Lab** (`/risk-lab`), inspect how the multimodal XGBoost model uses ENSO lag, rainfall departure, and NDVI anomalies to generate predictive agricultural drought scores with full SHAP interpretability.

---

## Evaluation Summary for HSC Judges

| Requirement | Implementation in VARUNA 2047 | Proof in Code |
| :--- | :--- | :--- |
| **Authentic Nationwide GIS** | All 36 States/UTs and 734 Districts mapped with real SOI geometries. | `data/processed/india_states.geojson`, `india_districts.geojson` |
| **Real Earth Observation** | ESA Copernicus Sentinel-2 L2A STAC/COG bi-temporal pixel subtraction. | `scripts/process_satellite_change.py`, `SatelliteComparisonSlider.tsx` |
| **Scientific Disclosures** | Labeled as candidate disturbance from NDVI change; no fake tree counts. | `UI_MAP_REDESIGN_AND_WORKER_FIX_REPORT.md`, `TECHNICAL_DESIGN_DOCUMENT.md` |
| **Explainable AI** | XGBoost risk model with TreeSHAP feature attributions on Telangana ground truth. | `ml/`, `models/saved/model_d_xgboost_multimodal.pkl` |
| **Code & Build Quality** | 35 passed pytest tests; Next.js 16 production build compiles with zero errors. | `docs/TESTING.md` |
