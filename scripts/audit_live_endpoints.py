"""
VARUNA 2047 - Independent Live Endpoints Auditor
Audits all FastAPI backend endpoints and Next.js frontend pages.
"""

import httpx
import json

backend_routes = [
    # Core Observational & Model Endpoints
    ("GET", "http://127.0.0.1:8000/api/health", None),
    ("GET", "http://127.0.0.1:8000/api/data/sources", None),
    ("GET", "http://127.0.0.1:8000/api/districts", None),
    ("GET", "http://127.0.0.1:8000/api/districts/WAR", None),
    ("GET", "http://127.0.0.1:8000/api/enso/history", None),
    ("GET", "http://127.0.0.1:8000/api/enso/current", None),
    ("GET", "http://127.0.0.1:8000/api/enso/events", None),
    ("GET", "http://127.0.0.1:8000/api/rainfall/history?district_id=WAR", None),
    ("GET", "http://127.0.0.1:8000/api/rainfall/anomalies?district_id=WAR", None),
    ("GET", "http://127.0.0.1:8000/api/satellite/layers", None),
    ("GET", "http://127.0.0.1:8000/api/satellite/metadata", None),
    ("GET", "http://127.0.0.1:8000/api/vegetation/history?district_id=WAR", None),
    ("GET", "http://127.0.0.1:8000/api/vegetation/anomalies", None),
    ("GET", "http://127.0.0.1:8000/api/models", None),
    ("GET", "http://127.0.0.1:8000/api/models/model_b_enso_lr/metrics", None),
    ("GET", "http://127.0.0.1:8000/api/models/model_d_xgboost_multimodal/features", None),
    ("POST", "http://127.0.0.1:8000/api/risk/predict", {"district_id": "WAR"}),
    ("POST", "http://127.0.0.1:8000/api/resilience/prioritize", {"risk_weight": 0.35, "vegetation_stress_weight": 0.25, "exposure_weight": 0.2, "irrigation_vulnerability_weight": 0.2}),
    ("POST", "http://127.0.0.1:8000/api/reports/generate", {"district_id": "WAR", "year": 2024}),

    # India Nationwide GIS Endpoints
    ("GET", "http://127.0.0.1:8000/api/india/states", None),
    ("GET", "http://127.0.0.1:8000/api/india/states/TS", None),
    ("GET", "http://127.0.0.1:8000/api/india/states/TS/districts", None),
    ("GET", "http://127.0.0.1:8000/api/india/districts/WAR", None),

    # ForestWatch Endpoints
    ("GET", "http://127.0.0.1:8000/api/forest/coverage", None),
    ("GET", "http://127.0.0.1:8000/api/forest/change?region_id=NATIONAL", None),
    ("GET", "http://127.0.0.1:8000/api/forest/loss/history?region_id=NATIONAL", None),
    ("GET", "http://127.0.0.1:8000/api/forest/loss/regions?region_type=states", None),
    ("GET", "http://127.0.0.1:8000/api/forest/satellite-scenes", None),
    ("GET", "http://127.0.0.1:8000/api/forest/change-map", None),
    ("GET", "http://127.0.0.1:8000/api/forest/provenance", None),
    ("POST", "http://127.0.0.1:8000/api/forest/compare", {"region_id": "WAR", "baseline_year": 2019, "recent_year": 2023, "canopy_class": "OF"}),
    ("POST", "http://127.0.0.1:8000/api/forest/reports/generate", {"region_id": "WAR", "region_type": "district", "include_satellite_comparison": True})
]

frontend_pages = [
    "/",
    "/explorer",
    "/enso",
    "/risk-lab",
    "/vegetation",
    "/resilience",
    "/reports",
    "/research",
    "/india",
    "/india/ts/war",
    "/forestwatch"
]

def audit():
    print("="*70)
    print("BACKEND ENDPOINTS AUDIT (http://127.0.0.1:8000)")
    print("="*70)
    backend_ok = True
    for method, url, body in backend_routes:
        path = url.replace("http://127.0.0.1:8000", "")
        try:
            if method == "GET":
                r = httpx.get(url, timeout=10)
            else:
                r = httpx.post(url, json=body, timeout=10)
            status = "PASS" if r.status_code == 200 else f"FAIL ({r.status_code})"
            if r.status_code != 200:
                backend_ok = False
            print(f"[{status}] {method:<4} {path:<48} -> {r.status_code} ({len(r.content)} bytes)")
        except Exception as e:
            backend_ok = False
            print(f"[FAIL] {method:<4} {path:<48} -> ERROR: {e}")

    print("\n" + "="*70)
    print("FRONTEND PAGES AUDIT (http://localhost:3000)")
    print("="*70)
    frontend_ok = True
    for path in frontend_pages:
        url = f"http://localhost:3000{path}"
        try:
            r = httpx.get(url, timeout=15)
            status = "PASS" if r.status_code == 200 else f"FAIL ({r.status_code})"
            if r.status_code != 200:
                frontend_ok = False
            print(f"[{status}] GET  {path:<48} -> {r.status_code} ({len(r.content)} bytes)")
        except Exception as e:
            frontend_ok = False
            print(f"[FAIL] GET  {path:<48} -> ERROR: {e}")

    print("="*70)
    if backend_ok and frontend_ok:
        print(f"ALL {len(backend_routes)} BACKEND ENDPOINTS AND {len(frontend_pages)} FRONTEND PAGES PASS LIVE AUDIT!")
    else:
        print("SOME CHECKS FAILED! Inspect the output above.")
    print("="*70)

if __name__ == "__main__":
    audit()
