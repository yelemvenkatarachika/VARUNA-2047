"""
VARUNA 2047 - Dataset Integrity & Live URL Auditor
Inspects downloaded files and live remote endpoints for NOAA, NASA, and ISRO.
"""

import os
import json
import httpx

DATASETS = [
    {
        "name": "NOAA CPC ONI Time-Series",
        "url": "https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt",
        "raw_file": "data/raw/enso/oni_raw.txt",
        "processed_file": "data/processed/enso_history.json"
    },
    {
        "name": "NASA POWER Agroclimatology (Warangal)",
        "url": "https://power.larc.nasa.gov/api/temporal/monthly/point?parameters=PRECTOTCORR&community=AG&longitude=79.59&latitude=17.97&format=JSON&start=2020&end=2023",
        "raw_file": "data/raw/rainfall/WAR_nasa_power.json",
        "processed_file": "data/processed/rainfall_history.json"
    },
    {
        "name": "ISRO Bhuvan Open Vector WMS",
        "url": "https://bhuvan-vec1.nrsc.gov.in/bhuvan/wms?SERVICE=WMS&REQUEST=GetCapabilities",
        "raw_file": "data/processed/isro_provenance.json",
        "processed_file": "data/processed/isro_provenance.json"
    }
]

def audit_datasets():
    print("="*70)
    print("EXTERNAL DATASET INTEGRITY & PROVENANCE AUDIT")
    print("="*70)

    for ds in DATASETS:
        print(f"\nAudit Target: {ds['name']}")
        print(f"  Source URL: {ds['url']}")
        
        # 1. Live URL test
        try:
            r = httpx.get(ds["url"], timeout=12.0, verify=False, follow_redirects=True)
            print(f"  Live URL Status: HTTP {r.status_code} (Content-Length: {len(r.content)} bytes)")
        except Exception as e:
            print(f"  Live URL Status: FAILED ({e})")

        # 2. Raw File on disk
        if os.path.exists(ds["raw_file"]):
            size = os.path.getsize(ds["raw_file"])
            print(f"  Raw File on Disk: {ds['raw_file']} ({size:,} bytes) - EXISTS")
        else:
            print(f"  Raw File on Disk: {ds['raw_file']} - MISSING")

        # 3. Processed File on disk
        if os.path.exists(ds["processed_file"]):
            size = os.path.getsize(ds["processed_file"])
            with open(ds["processed_file"], "r", encoding="utf-8") as f:
                data = json.load(f)
            rec_count = len(data.get("data", [])) or len(data.get("all_records", [])) or len(data.get("services", []))
            print(f"  Processed File: {ds['processed_file']} ({size:,} bytes, {rec_count} records) - VALID")
        else:
            print(f"  Processed File: {ds['processed_file']} - MISSING")

    print("\n" + "="*70)

if __name__ == "__main__":
    audit_datasets()
