# External Data Licenses & Usage Rights

**Project:** VARUNA 2047 — National Earth Intelligence for Agricultural and Environmental Resilience  
**Competition:** Hack for Social Cause — VBYLD 2027  
**Team:** bulls_eye  

This document details the licensing, provenance, terms of use, and redistribution rights for all external observational datasets, satellite imagery, geospatial administrative boundaries, and climate indices incorporated into or accessed by the VARUNA 2047 platform.

Original platform code is licensed separately under the [MIT License](file:///d:/RACHIKA/HFS/LICENSE).

---

## Directory of External Data Sources

| Dataset / Asset | Data Provider | License / Terms of Use | Commercial Use | Attribution Required | Redistribution Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Copernicus Sentinel-2 MSI** | European Space Agency (ESA) / European Commission | [Copernicus Open Access Policy](https://sentinels.copernicus.eu/web/sentinel/copernicus-data-and-information-policy) | Yes (Free) | Yes ("Contains modified Copernicus Sentinel data [year]") | Public / Open Data Archive |
| **Hansen Global Forest Change (GFC v1.11)** | Hansen / University of Maryland (UMD) / Google / USGS / NASA | [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) | Yes | Yes (Citation to Hansen et al. 2013) | Freely redistributable with attribution |
| **NOAA Oceanic Niño Index (ONI)** | National Oceanic and Atmospheric Administration (NOAA) CPC | [U.S. Public Domain / Open Access](https://www.noaa.gov/information-technology/open-data) | Yes | Yes (NOAA Climate Prediction Center) | Public domain |
| **NASA POWER Agroclimatology** | NASA Langley Research Center | [NASA Open Data Policy (Public Domain)](https://power.larc.nasa.gov/) | Yes | Yes (NASA POWER Project) | Public domain |
| **India Administrative Boundaries (States & Districts)** | Survey of India (SOI) / Registrar General of India (RGI) | [National Data Sharing and Accessibility Policy (NDSAP) / Open Government Data (OGD) India](https://data.gov.in/) | Permitted for research & non-commercial public analysis | Yes (Survey of India / Bharat Maps) | Derived GeoJSON geometries for visualization |
| **India State of Forest Report (ISFR)** | Forest Survey of India (FSI), Ministry of Environment, Forest and Climate Change (MoEFCC) | Published Government of India Official Statistics | Public citation permitted | Yes (Forest Survey of India, ISFR 2021) | Published official tables |
| **Esri Dark Gray Canvas Basemap** | Esri, DeLorme, FAO, NOAA, USGS | [Esri Master License Agreement / ArcGIS Online Terms of Use](https://www.esri.com/en-us/legal/terms/full-master-agreement) | Permitted for public non-commercial web map rendering | Embedded in tile attribution | Direct raster tile stream from public server |
| **MapLibre GL JS & Glyph Assets** | MapLibre Community / Open Source Contributors | [3-Clause BSD License](https://github.com/maplibre/maplibre-gl-js/blob/main/LICENSE.txt) | Yes | Yes | Permissive open source |

---

## Detailed Data Provider Policies

### 1. European Space Agency (ESA) — Copernicus Sentinel-2 MSI
- **Scope in VARUNA 2047:** Multi-spectral Level-2A Bottom-Of-Atmosphere (BOA) Surface Reflectance imagery for Tile `44QLE` (Warangal ecological corridor, baseline 2019 vs recent 2024).
- **Access Protocol:** Streamed from the public AWS Open Data Sponsorship Program (`https://sentinel-cogs.s3.us-west-2.amazonaws.com`).
- **License Notice:** *"Contains modified Copernicus Sentinel data (2019, 2024), processed by VARUNA 2047 change detection engine."*
- **Terms:** Unrestricted access to Sentinel data is provided pursuant to the European Union's Copernicus legal framework (Regulation EU No 377/2014 and Commission Delegated Regulation EU No 1159/2013).

### 2. Hansen / UMD / Google / USGS / NASA — Global Forest Change (30m)
- **Scope in VARUNA 2047:** Aggregated annual tree cover loss (2000–2023) at state and national administrative levels.
- **Citation:** Hansen, M. C., et al. (2013). "High-Resolution Global Maps of 21st-Century Forest Cover Change." *Science* 342 (6160): 850–853. Data updated through 2023.
- **Terms:** Provided under Creative Commons Attribution 4.0 International License (CC BY 4.0).
- **Redistribution:** Pre-processed regional tabular summaries are distributed in `data/processed/forest_loss_india.json`.

### 3. NOAA Climate Prediction Center — Oceanic Niño Index (ONI)
- **Scope in VARUNA 2047:** Monthly 3-month running mean of ERSST.v5 SST anomalies in the Niño 3.4 region from 1950 to 2024.
- **Terms:** As a work of the United States Government, NOAA CPC data is in the public domain and free of copyright restrictions under 17 U.S.C. § 105.
- **Redistribution:** Cached in `data/processed/enso_history.json`.

### 4. NASA POWER Agroclimatology Project
- **Scope in VARUNA 2047:** Monthly surface downward solar radiation, relative humidity, temperature extremes, and precipitation reanalysis for monitored agro-climatic zones.
- **Terms:** NASA POWER data is provided free of charge under the NASA Open Data Policy.
- **Redistribution:** Ingested into multimodal tabular datasets (`data/processed/model_features_dataset.csv`).

### 5. Survey of India (SOI) & Registrar General of India (RGI)
- **Scope in VARUNA 2047:** Nationwide administrative boundaries for 28 States, 8 Union Territories, and 734 Districts.
- **Reference Datum:** EPSG:4326 (WGS84).
- **Terms:** Administrative boundaries are synthesized from Survey of India open administrative publications and Census of India administrative atlases under the National Data Sharing and Accessibility Policy (NDSAP) published on `data.gov.in`.
- **Disclaimer:** Administrative boundaries depicted on VARUNA 2047 are for educational, research, and geospatial analytical visualization purposes under the Hack for Social Cause competition guidelines and do not constitute legal or political demarcation.

### 6. Forest Survey of India (FSI) — ISFR Baseline Statistics
- **Scope in VARUNA 2047:** Official state-level forest cover baselines (Very Dense Forest, Moderately Dense Forest, Open Forest) from the India State of Forest Report (ISFR 2021).
- **Terms:** Published official statistics of the Ministry of Environment, Forest and Climate Change (MoEFCC), Government of India.

---

## Code vs Data License Separation

```
VARUNA-2047 Repository
├── Original Code (.py, .ts, .tsx, .css, .sh)  ===> MIT License (see LICENSE)
├── Derived Aggregations & Model Weights        ===> MIT License / Open Research
└── External Observational & Boundary Data     ===> Governed by Individual Data Licenses (above)
```

No external proprietary or commercial datasets have been placed under the project's MIT License. Evaluators and researchers cloning this repository may freely inspect, modify, and run the platform code in compliance with the above open data policies.
