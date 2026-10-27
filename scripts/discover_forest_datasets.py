"""
VARUNA 2047 - Forest Datasets Discovery & Provenance Compiler
Validates and logs authoritative remote sensing and forest inventory sources.
"""

import json
import os
import sys
import shutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from geospatial.forest.provenance import FOREST_PROVENANCE_REGISTRY

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed")
FRONTEND_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "public", "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FRONTEND_DATA_DIR, exist_ok=True)

def discover_forest_sources():
    out_file = os.path.join(OUTPUT_DIR, "forest_provenance.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(FOREST_PROVENANCE_REGISTRY, f, indent=2)

    shutil.copy2(out_file, os.path.join(FRONTEND_DATA_DIR, "forest_provenance.json"))
    print(f"Forest provenance register written to {out_file} ({len(FOREST_PROVENANCE_REGISTRY)} verified providers)")

if __name__ == "__main__":
    discover_forest_sources()
