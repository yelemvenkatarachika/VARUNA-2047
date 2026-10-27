"""
VARUNA 2047 - Forest Loss Choropleth & Vector Tiles Generator
Merges boundary geometries with Hansen GFC and FSI loss data to generate
an interactive choropleth GeoJSON for map rendering.
"""

import json
import os
import shutil

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(ROOT_DIR, "data", "processed")
FRONTEND_DATA_DIR = os.path.join(ROOT_DIR, "frontend", "public", "data")

def build_choropleth():
    states_geo_file = os.path.join(PROCESSED_DIR, "india_states.geojson")
    loss_file = os.path.join(PROCESSED_DIR, "forest_loss_india.json")

    with open(states_geo_file, "r", encoding="utf-8") as f:
        states_geo = json.load(f)
    with open(loss_file, "r", encoding="utf-8") as f:
        loss_data = json.load(f)

    for feature in states_geo["features"]:
        sid = feature["properties"]["id"]
        s_loss = loss_data["states"].get(sid, {})
        feature["properties"]["baseline_forest_ha"] = s_loss.get("baseline_forest_ha", 0)
        feature["properties"]["loss_2023_ha"] = s_loss.get("loss_2023_ha", 0)
        feature["properties"]["loss_2022_ha"] = s_loss.get("loss_2022_ha", 0)
        feature["properties"]["loss_2021_ha"] = s_loss.get("loss_2021_ha", 0)
        feature["properties"]["loss_2020_ha"] = s_loss.get("loss_2020_ha", 0)
        feature["properties"]["total_loss_2001_2023_ha"] = s_loss.get("total_loss_2001_2023_ha", 0)

        baseline = max(1, s_loss.get("baseline_forest_ha", 1))
        feature["properties"]["loss_pct_2023"] = round((s_loss.get("loss_2023_ha", 0) / baseline) * 100.0, 3)

    out_file = os.path.join(PROCESSED_DIR, "forest_loss_choropleth.geojson")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(states_geo, f, indent=2)

    shutil.copy2(out_file, os.path.join(FRONTEND_DATA_DIR, "forest_loss_choropleth.geojson"))
    print(f"Generated forest loss choropleth GeoJSON at {out_file} ({len(states_geo['features'])} states)")

if __name__ == "__main__":
    build_choropleth()
