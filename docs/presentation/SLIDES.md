# VARUNA 2047: Presentation Slide Deck (7 Slides)

**Competition:** Hack for Social Cause — VBYLD 2027  
**Presentation Title:** VARUNA 2047: From Global Climate Signals to Local Agricultural Resilience  
**Subtitle:** Explainable Geospatial AI & Earth Observation for Viksit Bharat @ 2047  

---

## Slide 1: Project & National Vision
- **Project Identity:** VARUNA 2047 (*Viksit Bharat Agricultural Resilience Using National Earth Observation*)
- **Tagline:** From Global Climate Signals to Local Agricultural Resilience
- **Alignment with Viksit Bharat @ 2047:**
  - Transforming Indian agriculture into a climate-resilient, technologically sovereign backbone.
  - Empowering 120M+ smallholder farmers with early-warning intelligence.
  - Bridging equatorial Pacific ocean-atmosphere physics with mandal-level farm management.
- **Key Themes:** AI, GIS & Remote Sensing • UN SDGs 2 (Zero Hunger), 6 (Clean Water), 13 (Climate Action).

---

## Slide 2: Problem Statement & Target Beneficiaries
- **The Agrarian Crisis:**
  - Over 55% of Indian net sown area is rainfed and acutely vulnerable to monsoon deficit shocks.
  - El Niño elevates drought risks, yet local impacts diverge widely due to regional topography and Indian Ocean buffering.
  - Data exists across scientific silos (NOAA, NASA, ISRO), but agricultural officers lack integrated, explainable decision support before sowing begins.
- **Primary Beneficiaries:**
  - Small & marginal farmers (preventing seed and input capital loss).
  - District Agricultural Officers & Extension Workers (targeting contingency advisories).
  - Irrigation and Disaster Management Authorities (reservoir allocation and early drought alerts).

---

## Slide 3: Innovation & Technical Differentiation
- **What Sets VARUNA 2047 Apart:**
  - **Zero Fabrication Standard:** Authentic climate records (NOAA ONI 1950–2026, NASA POWER 1981–2024), live ISRO Bhuvan thematic layers, and transparently disclosed simulation demonstration rasters.
  - **Strict Pre-Monsoon Benchmark (May 31 Cutoff):** Zero target leakage; all predictors are observable strictly before monsoon onset.
  - **Explainable Multi-Criteria Prioritization:** Transparent mathematical scoring ($w_i \cdot S_i$) rather than black-box crop prescriptions.
  - **Public ISRO Compliance:** Verified active ISRO Bhuvan WMS integration (boundaries, SISDP-2 LULC, groundwater prospects) with honest disclosure of open-data access constraints.

---

## Slide 4: System Architecture & Data Engine
- **Decoupled Research Stack:**
  - **Frontend:** Next.js 16 (App Router), TypeScript, Tailwind CSS, MapLibre GL, Recharts.
  - **Backend API:** FastAPI, Pydantic V2, Uvicorn, ReportLab PDF Engine.
  - **Geospatial Processing:** Rasterio, Shapely, GeoPandas, PyProj (WGS84 & Web Mercator).
- **Multi-Modal Data Pipeline:**
  - NOAA CPC: 3-month running mean Niño 3.4 SST anomalies with official 5-season persistence.
  - NASA POWER: 44-year daily-to-monthly precipitation for 6 Telangana pilot districts.
  - ISRO Bhuvan: Live WMS layers for administrative boundaries, SISDP LULC, and groundwater prospects.
  - NASA EOSDIS GIBS: Authentic daily MODIS true-color satellite imagery tiles.
  - VARUNA Engine: Georeferenced biophysical simulation rasters for spatial pipeline demonstration.

---

## Slide 5: Working Prototype Demonstration
- **8 Dedicated Modules in Action:**
  1. **Mission Control:** Executive telemetry, active ENSO status, and district observable cards.
  2. **Earth Observation Explorer:** MapLibre interactive canvas with district polygons, ISRO thematic layers, and simulation raster overlays.
  3. **ENSO Observatory:** Interactive 74-year Niño 3.4 time-series chart and Walker circulation mechanics.
  4. **AI Risk Laboratory:** Dynamic pre-monsoon risk simulator, calibration curves, and SHAP explainability.
  5. **Agricultural Stress Explorer:** Rainfall-driven vegetative stress indices and VCI thresholds.
  6. **Resilience Planner:** Real-time priority matrix with adjustable policy weights.
  7. **Evidence Reports:** Automated, downloadable PDF dossiers for district officers.
  8. **Research & Transparency:** Full provenance register, UN SDG mapping, and reproducible code.

---

## Slide 6: Original AI Experiments & Scientific Evaluation
- **Methodological Rigor & Data Splits:**
  - Training: 1982–2014 ($N=198$ district-years) • Validation: 2015–2018 ($N=24$) • Untouched Held-out Test: 2019–2024 ($N=36$).
- **Untouched 2019–2024 Test Set Finding (Scientific Honesty):**
  - **Climatological Base Rate is Superior:** Brier score **0.0408** vs **0.1698–0.2182** for ML models.
  - Zero drought events occurred in Telangana during 2019–2024 ($N_+=0, N_-=36$).
  - ML models detected the 2019 & 2023 El Niño signals and elevated deficit risk, but droughts were mitigated by a positive Indian Ocean Dipole and Bay depressions, causing false alarms.
  - ROC-AUC is mathematically **undefined** on the untouched test set (requires both classes).
- **Multi-Window Post-Hoc Regime Analysis (2015–2024):**
  - Capturing the 2015 drought yields an exploratory ROC-AUC of 0.7830 for ENSO-LR, demonstrating teleconnection sensitivity while revealing the critical necessity of adding IOD predictors to prevent false alarms.

---

## Slide 7: Social Impact, Scalability & Viksit Bharat @ 2047
- **Measurable Socio-Economic Value:**
  - Enables contingency crop seed distribution (e.g. short-duration pulses) 3–4 weeks prior to monsoon failure.
  - Optimizes micro-irrigation subsidies and minor tank water storage in high-vulnerability mandals.
- **National Scalability Blueprint:**
  - Pilot validated across 6 key Telangana districts (Warangal, Hanamkonda, Karimnagar, Nizamabad, Adilabad, Khammam).
  - Scalable across Maharashtra (Vidarbha/Marathwada), Karnataka, and Andhra Pradesh using standard administrative GeoJSONs and automated satellite ingestion pipelines.
- **The Viksit Bharat Pledge:**
  - Scientific honesty over hype. Real Earth observation over synthetic mockups. Tangible resilience for Indian farmers.
