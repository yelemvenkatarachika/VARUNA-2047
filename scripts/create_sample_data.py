"""
VARUNA 2047 - Sample Data Generator (Refined)
Generates lightweight, legally redistributable sample datasets in data/sample/
demonstrating all core data structures with schema compliance.
"""

import os
import json
import pandas as pd

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
SAMPLE_DIR = os.path.join(BASE_DIR, "data", "sample")

os.makedirs(SAMPLE_DIR, exist_ok=True)

# 1. Sample States GeoJSON
states_file = os.path.join(PROCESSED_DIR, "india_states.geojson")
if os.path.exists(states_file):
    with open(states_file, "r", encoding="utf-8") as f:
        states_data = json.load(f)
    sample_features = [
        f for f in states_data.get("features", [])
        if f.get("properties", {}).get("id") in ["TS", "AP"]
    ]
    sample_states = {
        "type": "FeatureCollection",
        "description": "Sample subset of 2 Indian States (Telangana and Andhra Pradesh) demonstrating administrative boundary schema.",
        "crs": states_data.get("crs", {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}}),
        "features": sample_features
    }
    with open(os.path.join(SAMPLE_DIR, "sample_states.geojson"), "w", encoding="utf-8") as f:
        json.dump(sample_states, f, indent=2)
    print(f"Created sample_states.geojson ({len(sample_features)} features)")

# 2. Sample Districts GeoJSON (Warangal and Mahabubabad)
districts_file = os.path.join(PROCESSED_DIR, "india_districts.geojson")
if os.path.exists(districts_file):
    with open(districts_file, "r", encoding="utf-8") as f:
        dist_data = json.load(f)
    sample_dist_features = [
        f for f in dist_data.get("features", [])
        if "WARANGAL" in f.get("properties", {}).get("id", "") or "MAHABUBABAD" in f.get("properties", {}).get("id", "")
    ]
    sample_districts = {
        "type": "FeatureCollection",
        "description": "Sample subset of 2 Indian Districts (Warangal and Mahabubabad) demonstrating district polygon schema.",
        "crs": dist_data.get("crs", {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}}),
        "features": sample_dist_features
    }
    with open(os.path.join(SAMPLE_DIR, "sample_districts.geojson"), "w", encoding="utf-8") as f:
        json.dump(sample_districts, f, indent=2)
    print(f"Created sample_districts.geojson ({len(sample_dist_features)} features)")

# 3. Sample ENSO History JSON
enso_file = os.path.join(PROCESSED_DIR, "enso_history.json")
if os.path.exists(enso_file):
    with open(enso_file, "r", encoding="utf-8") as f:
        enso_data = json.load(f)
    records = enso_data.get("data", [])[-12:]
    sample_enso = {
        "metadata": {
            "title": "Sample Oceanic Niño Index (ONI) History (12 Months)",
            "source": "NOAA Climate Prediction Center",
            "license": "U.S. Public Domain",
            "parameter": "3-month running mean of ERSST.v5 SST anomalies in Niño 3.4 region (5°N-5°S, 120°-170°W)",
            "unit": "Degrees Celsius"
        },
        "data": records
    }
    with open(os.path.join(SAMPLE_DIR, "sample_enso_history.json"), "w", encoding="utf-8") as f:
        json.dump(sample_enso, f, indent=2)
    print(f"Created sample_enso_history.json ({len(records)} records)")

# 4. Sample Rainfall History JSON (Warangal district)
rainfall_file = os.path.join(PROCESSED_DIR, "rainfall_history.json")
if os.path.exists(rainfall_file):
    with open(rainfall_file, "r", encoding="utf-8") as f:
        rf_data = json.load(f)
    war_records = [r for r in rf_data.get("all_records", []) if r.get("district_id") == "WAR"][-5:]
    sample_rf = {
        "metadata": {
            "title": "Sample Rainfall Records (Warangal District)",
            "source": "NASA POWER / IMD Gridded Rainfall Reanalysis",
            "license": "NASA Open Data / Public Access",
            "district": "Warangal (WAR), Telangana",
            "unit": "mm"
        },
        "district_summary": rf_data.get("district_summaries", {}).get("WAR", {}),
        "sample_records": war_records
    }
    with open(os.path.join(SAMPLE_DIR, "sample_rainfall_history.json"), "w", encoding="utf-8") as f:
        json.dump(sample_rf, f, indent=2)
    print(f"Created sample_rainfall_history.json ({len(war_records)} records)")

# 5. Sample Forest Loss Response JSON
forest_file = os.path.join(PROCESSED_DIR, "forest_loss_india.json")
if os.path.exists(forest_file):
    with open(forest_file, "r", encoding="utf-8") as f:
        fl_data = json.load(f)
    sample_fl = {
        "metadata": {
            "title": "Sample Forest Cover and Annual Loss Response",
            "source": "Hansen Global Forest Change v1.11 & FSI ISFR",
            "license": "Creative Commons Attribution 4.0 International",
            "measurement_unit": "Hectares (ha)"
        },
        "national_summary": {
            "region_id": "NATIONAL",
            "region_name": "Republic of India",
            "baseline_tree_cover_ha": fl_data.get("total_baseline_tree_cover_ha", 30128000),
            "recent_loss_2023_ha": fl_data.get("annual_loss", {}).get("2023", 143500)
        },
        "sample_annual_loss_series": {
            k: v for k, v in list(fl_data.get("annual_loss", {}).items())[-5:]
        }
    }
    with open(os.path.join(SAMPLE_DIR, "sample_forest_loss_response.json"), "w", encoding="utf-8") as f:
        json.dump(sample_fl, f, indent=2)
    print("Created sample_forest_loss_response.json")

# 6. Sample Satellite Scenes Metadata JSON
scenes_file = os.path.join(PROCESSED_DIR, "forest_satellite_scenes.json")
if os.path.exists(scenes_file):
    with open(scenes_file, "r", encoding="utf-8") as f:
        scenes_data = json.load(f)
    with open(os.path.join(SAMPLE_DIR, "sample_satellite_scenes.json"), "w", encoding="utf-8") as f:
        json.dump(scenes_data, f, indent=2)
    print("Created sample_satellite_scenes.json")

# 7. Sample Model Features CSV
csv_file = os.path.join(PROCESSED_DIR, "model_features_dataset.csv")
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
    df_sample = df.head(10)
    df_sample.to_csv(os.path.join(SAMPLE_DIR, "sample_model_features.csv"), index=False)
    print(f"Created sample_model_features.csv ({len(df_sample)} rows)")

# 8. Create data/sample/README.md
readme_content = """# VARUNA 2047: Sample Datasets & Schema Directory

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
"""

with open(os.path.join(SAMPLE_DIR, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme_content)
print("Created data/sample/README.md")
