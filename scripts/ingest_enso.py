"""
VARUNA 2047 - NOAA ENSO Niño 3.4 / ONI Ingestion Pipeline
Fetches authentic historical ENSO data from NOAA Climate Prediction Center (CPC).
Implements official NOAA Oceanic Niño Index (ONI) persistence criteria:
- El Niño: ONI >= +0.5 °C for at least 5 consecutive overlapping seasons
- La Niña: ONI <= -0.5 °C for at least 5 consecutive overlapping seasons
- Neutral: All other periods

Source URL: https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt
Fallback Source: ERSSTv5 Nino 3.4 indices
"""

import os
import json
import httpx
import pandas as pd
import numpy as np
from datetime import datetime

NOAA_ONI_URL = "https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt"
RAW_CACHE_FILE = "data/raw/enso/oni_raw.txt"
OUTPUT_JSON = "data/processed/enso_history.json"
EVENTS_JSON = "data/processed/enso_events.json"

SEASONS_ORDER = ["DJF", "JFM", "FMA", "MAM", "AMJ", "JJA", "JAS", "ASO", "SON", "OND", "NDJ"]
SEASON_MONTH_MAP = {
    "DJF": 1, "JFM": 2, "FMA": 3, "MAM": 4, "AMJ": 5, "JJA": 6,
    "JAS": 7, "ASO": 8, "SON": 9, "OND": 10, "NDJ": 11, "DJF_NEXT": 12
}

def fetch_noaa_oni(force_refresh=False):
    os.makedirs("data/raw/enso", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)

    content = None
    if not force_refresh and os.path.exists(RAW_CACHE_FILE):
        print(f"Reading cached NOAA ONI data from {RAW_CACHE_FILE}")
        with open(RAW_CACHE_FILE, "r", encoding="utf-8") as f:
            content = f.read()

    if not content:
        print(f"Fetching authentic NOAA ONI data from {NOAA_ONI_URL}...")
        try:
            r = httpx.get(NOAA_ONI_URL, timeout=20.0, follow_redirects=True)
            r.raise_for_status()
            content = r.text
            with open(RAW_CACHE_FILE, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Saved {len(content)} bytes of NOAA raw data to {RAW_CACHE_FILE}")
        except Exception as e:
            print(f"Error fetching NOAA data: {e}")
            if os.path.exists(RAW_CACHE_FILE):
                print("Falling back to existing cache...")
                with open(RAW_CACHE_FILE, "r", encoding="utf-8") as f:
                    content = f.read()
            else:
                raise RuntimeError("Could not retrieve NOAA data and no cache exists.")

    return parse_noaa_oni(content)

def parse_noaa_oni(text_content):
    lines = text_content.strip().split("\n")
    data_rows = []
    header_found = False

    for line in lines:
        parts = line.strip().split()
        if not parts:
            continue
        # Header line usually has: SEAS YR TOTAL ANOM
        if "SEAS" in parts and "YR" in parts:
            header_found = True
            continue
        if len(parts) >= 4:
            try:
                season = parts[0]
                year = int(parts[1])
                total_sst = float(parts[2])
                anomaly = float(parts[3])
                data_rows.append({
                    "season": season,
                    "year": year,
                    "total_sst": total_sst,
                    "anomaly": anomaly
                })
            except ValueError:
                continue

    df = pd.DataFrame(data_rows)
    print(f"Parsed {len(df)} seasonal ONI observations ({df['year'].min()} to {df['year'].max()})")
    return df

def classify_enso_episodes(df):
    """
    Official NOAA CPC Episode Classification:
    Warm episode (El Niño): >= +0.5 °C for at least 5 consecutive overlapping seasons.
    Cold episode (La Niña): <= -0.5 °C for at least 5 consecutive overlapping seasons.
    """
    n = len(df)
    anom = df['anomaly'].values
    
    # Episode mask
    is_warm_threshold = anom >= 0.5
    is_cold_threshold = anom <= -0.5
    
    phase = ["Neutral"] * n
    
    # Identify warm runs >= 5
    run_start = None
    for i in range(n):
        if is_warm_threshold[i]:
            if run_start is None:
                run_start = i
        else:
            if run_start is not None:
                run_length = i - run_start
                if run_length >= 5:
                    for j in range(run_start, i):
                        phase[j] = "El Niño"
                run_start = None
    if run_start is not None and (n - run_start) >= 5:
        for j in range(run_start, n):
            phase[j] = "El Niño"

    # Identify cold runs >= 5
    run_start = None
    for i in range(n):
        if is_cold_threshold[i]:
            if run_start is None:
                run_start = i
        else:
            if run_start is not None:
                run_length = i - run_start
                if run_length >= 5:
                    for j in range(run_start, i):
                        phase[j] = "La Niña"
                run_start = None
    if run_start is not None and (n - run_start) >= 5:
        for j in range(run_start, n):
            phase[j] = "La Niña"

    df['phase'] = phase
    
    # Episode intensity classification for El Niño / La Niña
    intensity = ["Neutral"] * n
    for i in range(n):
        p = phase[i]
        val = anom[i]
        if p == "El Niño":
            if val >= 2.0:
                intensity[i] = "Very Strong El Niño"
            elif val >= 1.5:
                intensity[i] = "Strong El Niño"
            elif val >= 1.0:
                intensity[i] = "Moderate El Niño"
            else:
                intensity[i] = "Weak El Niño"
        elif p == "La Niña":
            if val <= -2.0:
                intensity[i] = "Very Strong La Niña"
            elif val <= -1.5:
                intensity[i] = "Strong La Niña"
            elif val <= -1.0:
                intensity[i] = "Moderate La Niña"
            else:
                intensity[i] = "Weak La Niña"
        else:
            intensity[i] = "Neutral"

    df['intensity'] = intensity
    return df

def extract_distinct_events(df):
    """Group continuous episodes into historical events."""
    events = []
    current_phase = None
    start_idx = 0

    for i in range(len(df)):
        p = df.iloc[i]['phase']
        if p != current_phase:
            if current_phase in ["El Niño", "La Niña"]:
                sub = df.iloc[start_idx:i]
                peak_anom = sub['anomaly'].max() if current_phase == "El Niño" else sub['anomaly'].min()
                events.append({
                    "phase": current_phase,
                    "start_season": sub.iloc[0]['season'],
                    "start_year": int(sub.iloc[0]['year']),
                    "end_season": sub.iloc[-1]['season'],
                    "end_year": int(sub.iloc[-1]['year']),
                    "duration_seasons": len(sub),
                    "peak_anomaly": round(float(peak_anom), 2),
                    "intensity": sub.loc[sub['anomaly'] == peak_anom, 'intensity'].iloc[0]
                })
            current_phase = p
            start_idx = i

    if current_phase in ["El Niño", "La Niña"]:
        sub = df.iloc[start_idx:]
        peak_anom = sub['anomaly'].max() if current_phase == "El Niño" else sub['anomaly'].min()
        events.append({
            "phase": current_phase,
            "start_season": sub.iloc[0]['season'],
            "start_year": int(sub.iloc[0]['year']),
            "end_season": sub.iloc[-1]['season'],
            "end_year": int(sub.iloc[-1]['year']),
            "duration_seasons": len(sub),
            "peak_anomaly": round(float(peak_anom), 2),
            "intensity": sub.loc[sub['anomaly'] == peak_anom, 'intensity'].iloc[0]
        })

    return events

def run_ingestion():
    df = fetch_noaa_oni()
    df = classify_enso_episodes(df)
    events = extract_distinct_events(df)

    # Build clean output records
    records = []
    for _, row in df.iterrows():
        records.append({
            "season": row["season"],
            "year": int(row["year"]),
            "total_sst": round(float(row["total_sst"]), 2),
            "anomaly": round(float(row["anomaly"]), 2),
            "phase": row["phase"],
            "intensity": row["intensity"]
        })

    metadata = {
        "provider": "NOAA Climate Prediction Center (CPC)",
        "product_name": "Oceanic Niño Index (ONI) - ERSST.v5 Niño 3.4 SST Anomalies",
        "source_url": NOAA_ONI_URL,
        "spatial_coverage": "Niño 3.4 Region (5°N-5°S, 120°-170°W)",
        "spatial_resolution": "Area-averaged gridded SST",
        "temporal_resolution": "3-month running mean (Monthly timestep)",
        "time_range": f"{df['year'].min()} to {df['year'].max()}",
        "total_observations": len(records),
        "total_historical_events": len(events),
        "retrieval_timestamp": datetime.utcnow().isoformat() + "Z",
        "classification_rule": "NOAA CPC official 5-consecutive-season threshold (+/- 0.5 °C)",
        "latest_observation": records[-1]
    }

    payload = {
        "metadata": metadata,
        "data": records
    }

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"Saved {len(records)} ENSO records to {OUTPUT_JSON}")

    with open(EVENTS_JSON, "w", encoding="utf-8") as f:
        json.dump({"metadata": metadata, "events": events}, f, indent=2)
    print(f"Saved {len(events)} classified historical ENSO events to {EVENTS_JSON}")

    return payload

if __name__ == "__main__":
    run_ingestion()
