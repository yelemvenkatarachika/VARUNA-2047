# VARUNA 2047: Video Demonstration Script (3–5 Minutes)

**Target Duration:** 4 minutes 15 seconds  
**Speaker:** Principal Lead / Geospatial AI Engineer  
**Live Application Target:** `http://localhost:3000` (Next.js) & `http://localhost:8000` (FastAPI)  

---

### [00:00 – 00:45] Scene 1: The Agrarian Challenge & Viksit Bharat @ 2047
- **Visual:** Mission Control Dashboard (`/`). Zoom in on the national vision banner and pilot district cards.
- **Narrator Voiceover:**
  > "Namaste. Welcome to **VARUNA 2047: Viksit Bharat Agricultural Resilience Using National Earth Observation**, built for Hack for Social Cause — VBYLD 2027.
  > In India, erratic monsoons and rainfall deficits pose an existential threat to small and marginal farmers. While global climate signals like the El Niño–Southern Oscillation are tracked worldwide, local agricultural officers lack explainable tools to translate these macro signals into proactive contingency planning before sowing begins.
  > VARUNA 2047 is designed with a strict scientific integrity directive: zero fabricated data, zero target leakage, and genuine Earth-observation evidence."

---

### [00:45 – 01:30] Scene 2: Earth Observation Explorer & ISRO Integration
- **Visual:** Navigate to `/explorer`. Toggle the live ISRO Bhuvan WMS layer. Switch raster layers from Pre-Monsoon May NDVI to Peak Monsoon August NDVI. Drag the opacity slider. Click on Warangal and Adilabad district polygons.
- **Narrator Voiceover:**
  > "Here in the **Earth Observation Explorer**, we render authentic administrative boundaries for our pilot region in Telangana, including Warangal, Hanamkonda, Karimnagar, Nizamabad, Adilabad, and Khammam.
  > Notice our live WMS layer served directly from **ISRO NRSC Bhuvan**, validating national cartography. Beneath it, we overlay georeferenced surface-reflectance NDVI rasters calibrated to **Copernicus Sentinel-2** Bands 4 and 8.
  > Clicking any district polygon reveals authentic coordinates, 1981–2010 climatological normals, and pre-monsoon dry season baseline vegetation. All raster operations are executed through an open-source geospatial engine using Rasterio and Shapely."

---

### [01:30 – 02:15] Scene 3: NOAA ENSO Teleconnections & Physical Mechanics
- **Visual:** Navigate to `/enso`. Hover over the 74-year interactive Niño 3.4 time-series chart. Toggle between 1980–2024 and 2000–2024. Point out the +0.5°C El Niño and -0.5°C La Niña threshold lines.
- **Narrator Voiceover:**
  > "In the **ENSO Climate Observatory**, we chart official monthly Sea Surface Temperature anomalies from NOAA CPC spanning 1950 to 2026.
  > Rather than naively assuming every El Niño causes severe drought, VARUNA 2047 implements the official NOAA five-consecutive-season persistence criterion and documents physical teleconnection non-linearities. For instance, during the 1997 Super El Niño, peninsular India was buffered by a positive Indian Ocean Dipole, yielding near-normal rains. Our platform clearly explains these mechanics to prevent false panic."

---

### [02:15 – 03:05] Scene 4: Original Machine Learning & Explainable AI
- **Visual:** Navigate to `/risk-lab`. Review the model ablation table. Highlight the held-out 10-year test ROC-AUC (0.7830). Inspect the SHAP feature ranking chart. Move the interactive sliders to simulate a warm +1.5°C Niño 3.4 anomaly and click 'Simulate Inference'.
- **Narrator Voiceover:**
  > "Moving to the **AI Risk Laboratory**, we benchmark four distinct models under rigorous chronological validation. We trained on 1982–2014 records and evaluated on the held-out 2015–2024 decade.
  > Crucially, every predictor is restricted to observations available on or before **May 31**—strictly prior to monsoon onset, preventing any target leakage.
  > Our regularized ENSO logistic baseline achieves a strong out-of-sample **ROC-AUC of 0.7830**. Using **SHAP TreeExplainer**, we reveal how pre-season Pacific anomalies and local pre-monsoon soil moisture drive deficit probabilities.
  > Using the interactive simulator, officers can test pre-season scenarios and receive immediate calibrated risk bands with empirical 90% confidence intervals."

---

### [03:05 – 03:50] Scene 5: Resilience Prioritization & Automated Evidence Dossiers
- **Visual:** Navigate to `/resilience`. Adjust the scoring weight sliders. Watch the districts re-rank dynamically. Then navigate to `/reports` and click 'Download Official PDF'. Show the generated PDF evidence dossier opening.
- **Narrator Voiceover:**
  > "In the **Resilience Planner**, we translate risk into policy action through transparent Multi-Criteria Decision Analysis. Planning authorities can adjust policy weights for deficit risk, satellite vegetation stress, crop acreage exposure, and rainfed vulnerability. Districts are ranked in real-time, pairing each location with specific contingency actions like farm pond audits or contingency seed pre-positioning.
  > Finally, in the **Evidence Reports** module, a single click compiles a complete research dossier into an official PDF via ReportLab, synthesizing climate normals, risk bounds, and scientific provenance statements for field distribution."

---

### [03:50 – 04:15] Scene 6: Conclusion & The Viksit Bharat Commitment
- **Visual:** Return to `/research`. Highlight UN SDGs 2, 6, 13 and the open-source reproducibility instructions.
- **Narrator Voiceover:**
  > "VARUNA 2047 proves that with genuine Earth observation, disciplined scientific methodology, and explainable AI, we can build the institutional resilience that Indian agriculture needs for the next quarter-century.
  > From global climate signals to local agricultural resilience—towards Viksit Bharat @ 2047. Thank you."
