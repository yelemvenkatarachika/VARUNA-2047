# VARUNA 2047: Sample Datasets & Schema Directory

**Path:** `data/sample/`  
**Purpose:** Lightweight, legally redistributable sample datasets demonstrating all core schemas used across the VARUNA 2047 platform.

These sample files allow developers, evaluators, and researchers to understand data structures, test API endpoints, and validate serialization without requiring multi-gigabyte raw satellite GeoTIFFs or full-resolution spatial catalogs.

---

## Sample Files Directory

| File | Format | Source / Attribution | Description |
| :--- | :--- | :--- | :--- |
| [`sample_states.geojson`](sample_states.geojson) | GeoJSON (EPSG:4326) | Survey of India / RGI | 2 state polygon boundaries (Telangana, Andhra Pradesh) with ISO/State IDs and bounding boxes. |
| [`sample_districts.geojson`](sample_districts.geojson) | GeoJSON (EPSG:4326) | Survey of India / RGI | 2 district polygon boundaries (Warangal, Mahabubabad) with census codes and spatial centroids. |
| [`sample_enso_history.json`](sample_enso_history.json) | JSON | NOAA Climate Prediction Center | 12 monthly ONI SST anomaly records with El Niño / La Niña / Neutral phase designations. |
| [`sample_rainfall_history.json`](sample_rainfall_history.json) | JSON | NASA POWER / IMD Reanalysis | Warangal district climatological normals, monthly precipitation arrays, and monsoon anomalies. |
| [`sample_forest_loss_response.json`](sample_forest_loss_response.json) | JSON | Hansen GFC v1.11 / FSI | National-level tree cover baseline and 5-year annual forest loss time series. |
| [`sample_satellite_scenes.json`](sample_satellite_scenes.json) | JSON | ESA Copernicus Sentinel-2 L2A | Baseline (2019) and recent (2024) Sentinel-2 scene IDs, bands, dNDVI parameters, and 236.21 ha disturbance quantification. |
| [`sample_model_features.csv`](sample_model_features.csv) | CSV | VARUNA 2047 Multimodal Pipeline | 10 sample feature rows demonstrating the 10 multimodal columns (ENSO lag, rainfall, NDVI, soil, irrigation). |

---

## Licensing & Redistribution Notice

- **GeoJSON Boundaries:** Derived from Survey of India public administrative data under the National Data Sharing and Accessibility Policy (NDSAP).
- **Satellite & Climatology Metadata:** Public domain (NOAA, NASA) and CC-BY 4.0 (ESA Copernicus, Hansen/UMD).
- **Synthetic Test Fixtures:** If any synthetic mock data is utilized in local unit testing, it is clearly designated with a `"synthetic": true` attribute. All files in this sample folder contain genuine observational subsets.
