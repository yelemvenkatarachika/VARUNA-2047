# VARUNA 2047: Public Source Data Provenance Register

**Project Title:** VARUNA 2047 — Viksit Bharat Agricultural Resilience Using National Earth Observation  
**Project Tagline:** From Global Climate Signals to Local Agricultural Resilience  
**Audit Timestamp:** October 2026 (Pre-Monsoon Evaluation Baseline)  

---

## 1. NOAA Oceanic Niño Index (ONI) & Niño 3.4 SST Anomalies

- **Data Provider:** National Oceanic and Atmospheric Administration (NOAA) Climate Prediction Center (CPC)
- **Product Name:** Oceanic Niño Index (ONI) based on ERSST.v5 (Extended Reconstructed Sea Surface Temperature)
- **Official Source URL:** [https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt](https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt)
- **Spatial Coverage:** Niño 3.4 Region (5°N–5°S, 120°–170°W)
- **Spatial Resolution:** Area-averaged gridded Sea Surface Temperature
- **Temporal Resolution:** 3-month running mean (Monthly timestep)
- **Time Range Ingested:** 1950 to 2026 (920 seasonal observations)
- **Retrieval Timestamp:** 2026-10-26T16:11:55Z
- **Processing Method:** Automated ASCII retrieval, monthly timestamp normalization, 3-month running mean anomaly computation.
- **Classification Rules:** Official NOAA CPC Episode Persistence Criteria:
  - **Warm Episode (El Niño):** ONI $\ge +0.5^\circ\text{C}$ for at least 5 consecutive overlapping seasons (e.g., DJF, JFM, FMA, MAM, AMJ).
  - **Cold Episode (La Niña):** ONI $\le -0.5^\circ\text{C}$ for at least 5 consecutive overlapping seasons.
  - **Neutral:** All other intervals.
- **Usage in VARUNA 2047:** Pre-monsoon features (`nino34_djf`, `nino34_mam`, `nino34_trend`, `enso_phase_mam`, `enso_persistence_seasons`) strictly restricted to observations on or before May 31.
- **License / Restrictions:** Public Domain (U.S. Government Open Data Policy).

---

## 2. NASA POWER Agroclimatology Precipitation Records

- **Data Provider:** National Aeronautics and Space Administration (NASA) Langley Research Center
- **Product Name:** Prediction Of Worldwide Energy Resources (POWER) Agroclimatology Methodology
- **Parameter Used:** `PRECTOTCORR` (Precipitation Corrected, mm/day)
- **Official Source URL:** [https://power.larc.nasa.gov/](https://power.larc.nasa.gov/)
- **Spatial Resolution:** $0.5^\circ \times 0.5^\circ$ Latitude / Longitude Grid
- **Temporal Resolution:** Daily aggregated to Monthly Totals
- **Geographic Coverage:** Telangana Pilot Districts:
  - Adilabad ($19.6641^\circ\text{N}, 78.5320^\circ\text{E}$)
  - Nizamabad ($18.6725^\circ\text{N}, 78.0941^\circ\text{E}$)
  - Karimnagar ($18.4386^\circ\text{N}, 79.1288^\circ\text{E}$)
  - Hanamkonda ($18.0135^\circ\text{N}, 79.5540^\circ\text{E}$)
  - Warangal ($17.9689^\circ\text{N}, 79.5941^\circ\text{E}$)
  - Khammam ($17.2473^\circ\text{N}, 80.1514^\circ\text{E}$)
- **Time Range Ingested:** 1981 to 2024 (44 continuous years)
- **Processing Method:** Point spatial query, daily rate multiplication by days per calendar month (with leap year handling), calculation of pre-monsoon total (MAM: Mar-May) and Southwest Monsoon total (JJAS: Jun-Sep).
- **Climatological Reference Baseline:** 1981–2010 (30-year WMO Standard Normal).
- **Target Event Definition:** Deficit Event $y=1$ if Kharif JJAS rainfall $< 80\%$ of 1981–2010 district climatological mean ($>20\%$ deficit, standard IMD meteorological drought threshold).
- **License / Restrictions:** NASA Open Data Policy (Unrestricted scientific use).

---

## 3. ISRO Earth Observation & Geospatial Web Services Audit

- **Data Providers Investigated:**
  - ISRO National Remote Sensing Centre (NRSC) Bhuvan: [https://bhuvan.nrsc.gov.in/](https://bhuvan.nrsc.gov.in/)
  - ISRO Space Applications Centre (SAC) VEDAS: [https://vedas.sac.gov.in/](https://vedas.sac.gov.in/)
  - ISRO Space Applications Centre (SAC) MOSDAC: [https://www.mosdac.gov.in/](https://www.mosdac.gov.in/)
  - ISRO Bhoonidhi Data Dissemination Portal: [https://bhoonidhi.nrsc.gov.in/](https://bhoonidhi.nrsc.gov.in/)
- **Technical Audit & Discovery Script:** `scripts/discover_isro.py` executed live.
- **Audit Findings:**
  1. **ISRO Bhuvan Open Vector WMS (`https://bhuvan-vec1.nrsc.gov.in/bhuvan/wms`):** Verified active (HTTP 200). Permitted OGC WMS GetCapabilities parsed.
  2. **Verified Authentic ISRO Thematic Layers:**
     - `sisdpv2:TS_Warangal_lulc_v2`: ISRO NRSC Space Based Information Support for Decentralised Planning (SISDP-2) 1:50,000 Land Use / Land Cover (Verified HTTP 200 PNG).
     - `gw:TELANGANA_PRE`: ISRO NRSC Rajiv Gandhi National Drinking Water Mission (RGNDWM) Ground Water Prospects (Pre-Monsoon) (Verified HTTP 200 PNG).
     - `bhuvan:telangana_district_boundary`: ISRO NRSC Official District Administrative Boundaries (Verified HTTP 200).
  3. **Raw Multi-Decadal Pixel Rasters:** ISRO Bhoonidhi requires user-authenticated single-sign-on (SSO) and CAPTCHA tokens for downloading raw multi-spectral GeoTIFF arrays, preventing automated headless pipeline ingestion.
- **Scientific Integrity Compliance:** As per guidelines, VARUNA 2047 does not scrape protected endpoints or bypass access controls. Bhuvan is served via official public WMS for visualization and thematic contextualization.
- **Attribution Statement:** "Indian administrative base layers, SISDP LULC, and Ground Water Prospects served via ISRO / NRSC Bhuvan Open Web GIS."

---

## 4. VARUNA Biophysical Simulation Engine (Spatial Demonstration Rasters)

- **Provider:** VARUNA Biophysical Simulation Engine (Local Spatial Engine)
- **Purpose:** Demonstration of Rasterio georeferencing, polygon zonal statistics masking, and MapLibre SVG layer rendering.
- **Sensor Analog:** Modeled after ESA Copernicus Sentinel-2 MSI (B4 Red 665nm, B8 NIR 842nm) and NASA MODIS surface reflectance characteristics.
- **Mathematical Formula:**
  $$\text{NDVI} = \frac{\text{NIR} - \text{Red}}{\text{NIR} + \text{Red}}$$
  Modeled across the Deccan plateau pilot bounding box ($16.8^\circ\text{N}–20.2^\circ\text{N}, 77.5^\circ\text{E}–81.0^\circ\text{E}$) using elevation, river valley proximity, and agro-ecological parameters.
- **Rasters Produced:**
  1. `ndvi_premonsoon_may.tif`: `[SIMULATION]` Modeled pre-monsoon dry season baseline (bare soil & dry scrub).
  2. `ndvi_monsoon_peak.tif`: `[SIMULATION]` Modeled peak Kharif vegetative canopy flush (active chlorophyll absorption).
  3. `ndvi_monsoon_drought_scenario.tif`: `[SIMULATION]` Modeled drought stress scenario.
  4. `ndvi_anomaly_map.tif`: `[SIMULATION]` Difference grid between normal flush and drought scenario.
- **Observational Satellite Imagery:** Authentic daily observational satellite tiles are accessed via **NASA EOSDIS GIBS** (`MODIS_Terra_CorrectedReflectance_TrueColor`).
- **Temporal Coverage Clarification:** Operational Copernicus Sentinel-2 was launched in 2015 and Terra MODIS in 1999. They do not cover 1982–2014. The historical pre-monsoon NDVI series (1982–2024) in `vegetation_history.json` is a synthetic rainfall-driven proxy, NOT direct satellite observations.
- **License / Restrictions:** MIT Open Access. Transparently disclosed as synthetic simulation grids.
