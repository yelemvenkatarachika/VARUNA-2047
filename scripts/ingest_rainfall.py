"""
VARUNA 2047 - Authentic NASA Precipitation Ingestion Pipeline
Fetches historical monthly precipitation records from NASA POWER (Prediction Of Worldwide Energy Resources)
Parameter: PRECTOTCORR (Precipitation Corrected, mm/day)
Pilot Districts: Adilabad, Nizamabad, Karimnagar, Hanamkonda, Warangal, Khammam (Telangana, India)
Time Span: 1981 to 2024 (44 continuous years)

Calculates:
- Monthly precipitation totals (mm)
- Pre-monsoon (MAM: Mar-Apr-May) totals (mm)
- Southwest Monsoon (JJAS: Jun-Jul-Aug-Sep) totals (mm)
- 1981-2010 Climatological Reference Mean & Standard Deviation
- Percentage departure / anomaly relative to 1981-2010 normal
- Deficit Event indicator: JJAS rainfall < 80% of climatological mean (< -20% anomaly)
"""

import os
import json
import calendar
import time
import httpx
import pandas as pd
import numpy as np
from datetime import datetime, timezone

RAW_DIR = "data/raw/rainfall"
OUTPUT_FILE = "data/processed/rainfall_history.json"
DISTRICTS_FILE = "data/processed/districts_metadata.json"

DAYS_IN_MONTH = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def get_days_in_month(year, month):
    return calendar.monthrange(year, month)[1]

def fetch_district_precipitation(district, start_year=1981, end_year=2024, force_refresh=False):
    os.makedirs(RAW_DIR, exist_ok=True)
    cache_path = os.path.join(RAW_DIR, f"{district['id']}_nasa_power.json")

    data = None
    if not force_refresh and os.path.exists(cache_path):
        print(f"Loading cached NASA precipitation for {district['name']} ({district['id']})")
        with open(cache_path, "r", encoding="utf-8") as f:
            data = json.load(f)

    if not data:
        url = (
            f"https://power.larc.nasa.gov/api/temporal/monthly/point?"
            f"parameters=PRECTOTCORR&community=AG"
            f"&longitude={district['lon']}&latitude={district['lat']}"
            f"&format=JSON&start={start_year}&end={end_year}"
        )
        print(f"Fetching NASA POWER precipitation for {district['name']} ({district['id']}) from {url}...")
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                with httpx.Client(timeout=30.0) as client:
                    resp = client.get(url)
                    resp.raise_for_status()
                    data = resp.json()
                    with open(cache_path, "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=2)
                    print(f"Successfully cached data for {district['name']}")
                    time.sleep(1.0) # Respect rate limits
                    break
            except Exception as e:
                print(f"Attempt {attempt+1} failed for {district['name']}: {e}")
                if attempt == max_retries - 1:
                    raise RuntimeError(f"Could not retrieve NASA data for {district['name']}: {e}")
                time.sleep(2.0 * (attempt + 1))

    return parse_nasa_rainfall(district, data, start_year, end_year)

def parse_nasa_rainfall(district, raw_json, start_year=1981, end_year=2024):
    param_data = raw_json.get("properties", {}).get("parameter", {}).get("PRECTOTCORR", {})
    
    annual_records = []
    
    for yr in range(start_year, end_year + 1):
        monthly_mm = {}
        monthly_mm_day = {}
        for m in range(1, 13):
            key = f"{yr}{m:02d}"
            val = param_data.get(key, None)
            if val is not None and val != -999.0:
                days = get_days_in_month(yr, m)
                monthly_mm[m] = round(val * days, 2)
                monthly_mm_day[m] = round(val, 2)
            else:
                monthly_mm[m] = 0.0
                monthly_mm_day[m] = 0.0

        # Pre-monsoon: MAM (Mar, Apr, May)
        mam_rainfall = round(sum(monthly_mm[m] for m in [3, 4, 5]), 2)
        
        # Southwest Monsoon: JJAS (Jun, Jul, Aug, Sep)
        jjas_rainfall = round(sum(monthly_mm[m] for m in [6, 7, 8, 9]), 2)
        
        # Annual
        annual_rainfall = round(sum(monthly_mm.values()), 2)

        annual_records.append({
            "district_id": district["id"],
            "district_name": district["name"],
            "year": yr,
            "monthly_rainfall_mm": [monthly_mm[m] for m in range(1, 13)],
            "premonsoon_mam_mm": mam_rainfall,
            "monsoon_jjas_mm": jjas_rainfall,
            "annual_mm": annual_rainfall
        })

    # Compute 1981-2010 reference climatology (standard 30-year WMO baseline)
    ref_records = [r for r in annual_records if 1981 <= r["year"] <= 2010]
    jjas_values = [r["monsoon_jjas_mm"] for r in ref_records]
    mam_values = [r["premonsoon_mam_mm"] for r in ref_records]

    normal_jjas_mean = round(float(np.mean(jjas_values)), 2)
    normal_jjas_std = round(float(np.std(jjas_values)), 2)
    normal_mam_mean = round(float(np.mean(mam_values)), 2)
    
    # Drought / Deficit threshold: < 80% of normal (i.e. > 20% deficit)
    deficit_threshold_mm = round(0.80 * normal_jjas_mean, 2)

    # Annotate records with anomalies and target classification
    processed_records = []
    for r in annual_records:
        jjas = r["monsoon_jjas_mm"]
        anomaly_pct = round(((jjas - normal_jjas_mean) / normal_jjas_mean) * 100.0, 2)
        anomaly_mm = round(jjas - normal_jjas_mean, 2)
        is_deficit = 1 if jjas < deficit_threshold_mm else 0
        
        # Standard IMD Rainfall Categories:
        # Excess: +20% or more
        # Normal: -19% to +19%
        # Deficit: -20% to -59%
        # Severe Deficit: -60% or lower
        if anomaly_pct >= 20.0:
            category = "Excess"
        elif anomaly_pct >= -19.0:
            category = "Normal"
        elif anomaly_pct >= -59.0:
            category = "Deficit"
        else:
            category = "Severe Deficit"

        r_copy = dict(r)
        r_copy.update({
            "normal_jjas_mean_mm": normal_jjas_mean,
            "normal_jjas_std_mm": normal_jjas_std,
            "normal_mam_mean_mm": normal_mam_mean,
            "deficit_threshold_mm": deficit_threshold_mm,
            "monsoon_anomaly_mm": anomaly_mm,
            "monsoon_anomaly_pct": anomaly_pct,
            "is_deficit_event": is_deficit,
            "rainfall_category": category
        })
        processed_records.append(r_copy)

    summary = {
        "district_id": district["id"],
        "district_name": district["name"],
        "lat": district["lat"],
        "lon": district["lon"],
        "reference_period": "1981-2010",
        "climatological_normal_jjas_mm": normal_jjas_mean,
        "climatological_std_jjas_mm": normal_jjas_std,
        "deficit_threshold_mm": deficit_threshold_mm,
        "total_years_analyzed": len(annual_records),
        "total_deficit_years": sum(1 for r in processed_records if r["is_deficit_event"] == 1),
        "deficit_frequency_pct": round((sum(1 for r in processed_records if r["is_deficit_event"] == 1) / len(processed_records)) * 100.0, 1),
        "records": processed_records
    }
    return summary

def run_ingestion():
    with open(DISTRICTS_FILE, "r", encoding="utf-8") as f:
        districts = json.load(f)

    all_district_summaries = {}
    flat_annual_records = []

    for d in districts:
        summary = fetch_district_precipitation(d)
        all_district_summaries[d["id"]] = summary
        flat_annual_records.extend(summary["records"])

    metadata = {
        "provider": "NASA Langley Research Center",
        "product_name": "NASA POWER (Prediction Of Worldwide Energy Resources) Agroclimatology",
        "parameter": "PRECTOTCORR (Precipitation Corrected)",
        "source_url": "https://power.larc.nasa.gov/",
        "spatial_resolution": "0.5° x 0.5° Latitude/Longitude Grid",
        "temporal_resolution": "Monthly Aggregated",
        "time_span": "1981-2024 (44 years)",
        "target_definition": "Monsoon JJAS rainfall < 80% of 1981-2010 Climatological Reference Mean (IMD Deficit Benchmark)",
        "districts_covered": [d["name"] for d in districts],
        "generated_at": datetime.now(timezone.utc).isoformat()
    }

    final_payload = {
        "metadata": metadata,
        "district_summaries": all_district_summaries,
        "all_records": flat_annual_records
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final_payload, f, indent=2)
    print(f"Saved complete authentic rainfall history for 6 districts (1981-2024) to {OUTPUT_FILE}")
    return final_payload

if __name__ == "__main__":
    run_ingestion()
