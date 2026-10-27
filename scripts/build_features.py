"""
VARUNA 2047 - Feature Engineering Pipeline
Combines NOAA ENSO observations, NASA POWER precipitation records,
satellite vegetation indices, and district geographic attributes.

CRITICAL SCIENTIFIC INTEGRITY RULES:
1. Forecast Issuance Date: May 31 strictly prior to the Southwest Monsoon (JJAS).
2. All predictor features must be observable on or before May 31.
3. No target leakage: No JJAS rainfall, August vegetation, or post-May data in X.
4. Target variable y: 1 if Kharif JJAS rainfall < 80% of 1981-2010 normal (Deficit Event), 0 otherwise.
5. Chronological splitting:
   - Train: 1982-2014 (33 years)
   - Val:   2015-2018 (4 years)
   - Test:  2019-2024 (6 years)
"""

import os
import sys
import json
import pandas as pd
import numpy as np
from datetime import datetime, timezone

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

ENSO_FILE = "data/processed/enso_history.json"
RAINFALL_FILE = "data/processed/rainfall_history.json"
VEGETATION_FILE = "data/processed/vegetation_history.json"
DISTRICTS_FILE = "data/processed/districts_metadata.json"
FEATURES_OUTPUT = "data/processed/model_features_dataset.csv"
SCHEMA_OUTPUT = "data/processed/feature_schema.json"

def build_features():
    # 1. Load Datasets
    with open(ENSO_FILE, "r", encoding="utf-8") as f:
        enso_data = json.load(f)["data"]
    with open(RAINFALL_FILE, "r", encoding="utf-8") as f:
        rf_data = json.load(f)
    with open(VEGETATION_FILE, "r", encoding="utf-8") as f:
        veg_data = json.load(f)["annual_records"]
    with open(DISTRICTS_FILE, "r", encoding="utf-8") as f:
        dist_meta = {d["id"]: d for d in json.load(f)}

    # Index ENSO by (year, season)
    enso_dict = {}
    for obs in enso_data:
        enso_dict[(obs["year"], obs["season"])] = obs

    # Index Vegetation by (district_id, year)
    veg_dict = {}
    for v in veg_data:
        veg_dict[(v["district_id"], v["year"])] = v

    # Organize Rainfall by district and year
    rf_by_dist = {}
    for r in rf_data["all_records"]:
        rf_by_dist[(r["district_id"], r["year"])] = r

    rows = []
    # Build dataset for 1982 to 2024 (1982 allows 1-year lag from 1981)
    for yr in range(1982, 2025):
        # Retrieve pre-season ENSO features observable by May 31
        # DJF is December of previous year through February of target year
        # In NOAA tables, DJF for year Y corresponds to Dec(Y-1)-Jan(Y)-Feb(Y)
        djf_obs = enso_dict.get((yr, "DJF"), {})
        mam_obs = enso_dict.get((yr, "MAM"), {})

        nino34_djf = djf_obs.get("anomaly", 0.0)
        nino34_mam = mam_obs.get("anomaly", 0.0)
        nino34_trend = round(nino34_mam - nino34_djf, 3)
        
        mam_phase_str = mam_obs.get("phase", "Neutral")
        # Numerical encoding of ENSO phase: El Niño = +1, Neutral = 0, La Niña = -1
        phase_num = 1 if mam_phase_str == "El Niño" else (-1 if mam_phase_str == "La Niña" else 0)

        # Persistence: approximate consecutive seasons with same sign anomaly up to MAM
        persistence = 1
        for check_seas in ["FMA", "JFM", "DJF"]:
            past_obs = enso_dict.get((yr, check_seas), {})
            if np.sign(past_obs.get("anomaly", 0)) == np.sign(nino34_mam) and abs(past_obs.get("anomaly", 0)) >= 0.5:
                persistence += 1
            else:
                break

        for dist_id, dinfo in dist_meta.items():
            curr_rf = rf_by_dist.get((dist_id, yr), {})
            prev_rf = rf_by_dist.get((dist_id, yr - 1), {})
            curr_veg = veg_dict.get((dist_id, yr), {})

            # Target: 1 if Kharif JJAS rainfall < 80% of normal, else 0
            y_target = curr_rf.get("is_deficit_event", 0)
            actual_jjas_rainfall = curr_rf.get("monsoon_jjas_mm", 0.0)
            normal_jjas_mean = curr_rf.get("normal_jjas_mean_mm", 850.0)
            anomaly_pct = curr_rf.get("monsoon_anomaly_pct", 0.0)

            # Pre-season features (Strictly observable by May 31)
            mam_rainfall = curr_rf.get("premonsoon_mam_mm", 45.0)
            normal_mam = curr_rf.get("normal_mam_mean_mm", 45.0)
            mam_rf_anomaly = round(mam_rainfall - normal_mam, 2)

            prev_jjas_rf = prev_rf.get("monsoon_jjas_mm", normal_jjas_mean)
            prev_is_deficit = prev_rf.get("is_deficit_event", 0)

            preseason_ndvi = curr_veg.get("preseason_may_ndvi", 0.25)
            # NDVI anomaly relative to district mean May NDVI
            ndvi_anomaly = round(preseason_ndvi - 0.25, 3)

            # Determine Chronological Split
            if yr <= 2014:
                split = "train"
            elif yr <= 2018:
                split = "val"
            else:
                split = "test"

            rows.append({
                # Metadata / Identifiers
                "year": yr,
                "district_id": dist_id,
                "district_name": dinfo["name"],
                "split": split,

                # ENSO Feature Group
                "nino34_djf": nino34_djf,
                "nino34_mam": nino34_mam,
                "nino34_trend": nino34_trend,
                "enso_phase_mam": phase_num,
                "enso_persistence_seasons": persistence,

                # Climate Feature Group (observable by May 31)
                "preseason_rainfall_mam_mm": mam_rainfall,
                "preseason_rainfall_mam_anom_mm": mam_rf_anomaly,
                "prev_year_jjas_rainfall_mm": prev_jjas_rf,
                "prev_year_was_deficit": prev_is_deficit,

                # Satellite Feature Group (observable by May 31)
                "preseason_may_ndvi": preseason_ndvi,
                "preseason_may_ndvi_anomaly": ndvi_anomaly,

                # Geographic / Exposure Feature Group
                "district_lat": dinfo["lat"],
                "district_lon": dinfo["lon"],
                "elevation_m": dinfo["elevation_m"],
                "irrigation_coverage_pct": dinfo["irrigation_coverage_pct"],
                "net_sown_area_ha": dinfo["net_sown_area_ha"],

                # Target & Evaluation Observables (Excluded from X during training)
                "actual_jjas_rainfall_mm": actual_jjas_rainfall,
                "normal_jjas_mean_mm": normal_jjas_mean,
                "monsoon_anomaly_pct": anomaly_pct,
                "y_deficit_event": y_target
            })

    df = pd.DataFrame(rows)
    df.to_csv(FEATURES_OUTPUT, index=False)
    print(f"Engineered feature dataset with {len(df)} samples saved to {FEATURES_OUTPUT}")

    # Feature Schema & Ablation Groups Definition
    feature_schema = {
        "issuance_date": "May 31 (Strict pre-monsoon cutoff)",
        "target_variable": "y_deficit_event (1 if JJAS rainfall < 80% of 1981-2010 normal, 0 otherwise)",
        "splits": {
            "train": "1982-2014 (33 years, 198 district-years)",
            "validation": "2015-2018 (4 years, 24 district-years)",
            "test": "2019-2024 (6 years, 36 district-years)"
        },
        "feature_groups": {
            "group_a_climatology": [],
            "group_b_enso_only": [
                "nino34_djf", "nino34_mam", "nino34_trend", "enso_phase_mam", "enso_persistence_seasons"
            ],
            "group_c_enso_climate": [
                "nino34_djf", "nino34_mam", "nino34_trend", "enso_phase_mam", "enso_persistence_seasons",
                "preseason_rainfall_mam_mm", "preseason_rainfall_mam_anom_mm", "prev_year_jjas_rainfall_mm", "prev_year_was_deficit"
            ],
            "group_d_full_multimodal": [
                "nino34_djf", "nino34_mam", "nino34_trend", "enso_phase_mam", "enso_persistence_seasons",
                "preseason_rainfall_mam_mm", "preseason_rainfall_mam_anom_mm", "prev_year_jjas_rainfall_mm", "prev_year_was_deficit",
                "preseason_may_ndvi", "preseason_may_ndvi_anomaly",
                "district_lat", "district_lon", "elevation_m", "irrigation_coverage_pct", "net_sown_area_ha"
            ]
        },
        "generated_at": datetime.now(timezone.utc).isoformat()
    }

    with open(SCHEMA_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(feature_schema, f, indent=2)
    print(f"Saved feature schema to {SCHEMA_OUTPUT}")

    return df

if __name__ == "__main__":
    build_features()
