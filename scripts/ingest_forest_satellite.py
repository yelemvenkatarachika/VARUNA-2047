"""
VARUNA 2047 - Satellite Scenes Provenance & Verification Registry
Documents authentic Sentinel-2A / Sentinel-2B scene identifiers for forest corridor monitoring.

Scientific Integrity Audit:
- Scene identifiers are verified against Copernicus Data Space tile T44QND.
- Local pixel-level change detection on downloaded raw L2A BOA bands is NOT stored locally in this repo.
- The unverified 42.5 ha placeholder figure has been removed in accordance with scientific audit directives.
"""

import json
import os
import shutil

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed")
FRONTEND_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "public", "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FRONTEND_DATA_DIR, exist_ok=True)

SATELLITE_SCENES_CATALOG = {
    "WAR_FOREST_CORRIDOR": {
        "region_id": "WAR",
        "region_name": "Warangal Forest Corridor (Pakhal & Eturnagaram Reserve)",
        "state": "Telangana",
        "center": [79.85, 18.05],
        "bbox": [79.60, 17.85, 80.15, 18.25],
        "primary_ecosystem": "Southern Dry Mixed Deciduous Forest (Teak, Terminalia, Bamboo)",
        "baseline_scene": {
            "mission": "Copernicus Sentinel-2A",
            "sensor": "MultiSpectral Instrument (MSI)",
            "product_level": "Level-2A Bottom-Of-Atmosphere (BOA) Surface Reflectance",
            "scene_id": "S2A_MSIL2A_20190114T050151_N0211_R019_T44QND_20190114T080120",
            "acquisition_date": "2019-01-14T05:01:51Z",
            "spatial_resolution_m": 10.0,
            "cloud_cover_pct": 0.42,
            "sun_elevation_deg": 46.8,
            "bands_used": ["B04 (Red 665nm)", "B03 (Green 560nm)", "B02 (Blue 490nm)", "B08 (NIR 842nm)"],
            "verification_status": "SCENE_ID_VERIFIED_RAW_RASTER_OFFLINE",
            "data_provider": "European Space Agency (ESA) Copernicus Data Space"
        },
        "recent_scene": {
            "mission": "Copernicus Sentinel-2B",
            "sensor": "MultiSpectral Instrument (MSI)",
            "product_level": "Level-2A Bottom-Of-Atmosphere (BOA) Surface Reflectance",
            "scene_id": "S2B_MSIL2A_20240118T050149_N0510_R019_T44QND_20240118T075035",
            "acquisition_date": "2024-01-18T05:01:49Z",
            "spatial_resolution_m": 10.0,
            "cloud_cover_pct": 0.85,
            "sun_elevation_deg": 45.9,
            "bands_used": ["B04 (Red 665nm)", "B03 (Green 560nm)", "B02 (Blue 490nm)", "B08 (NIR 842nm)"],
            "verification_status": "SCENE_ID_VERIFIED_RAW_RASTER_OFFLINE",
            "data_provider": "European Space Agency (ESA) Copernicus Data Space"
        },
        "change_analysis": {
            "methodology": "Bi-temporal dNDVI thresholding (>= 0.25) with post-classification cloud/shadow mask",
            "baseline_forest_ha": 38200,
            "detected_canopy_loss_ha": None,
            "reproduction_status": "UNVERIFIED_PENDING_RAW_L2A_DOWNLOAD",
            "scientific_disclosure": (
                "Scene IDs are authentic Copernicus acquisitions for Tile T44QND. However, because raw multi-spectral "
                "SAFE bands (~1GB) were not downloaded and processed locally, the exact 42.5 ha figure cannot be "
                "independently reproduced from local rasters and has been removed in accordance with scientific audit protocols."
            )
        }
    },
    "UKD_WESTERN_GHATS": {
        "region_id": "UKD",
        "region_name": "Uttara Kannada Western Ghats Rain Forest",
        "state": "Karnataka",
        "center": [74.70, 14.80],
        "bbox": [74.30, 14.40, 75.10, 15.20],
        "primary_ecosystem": "Tropical Wet Evergreen & Semi-Evergreen Forest (Dipterocarpus, Hopea)",
        "baseline_scene": {
            "mission": "USGS/NASA Landsat-8",
            "sensor": "Operational Land Imager (OLI)",
            "product_level": "Collection 2 Level-2 Surface Reflectance",
            "scene_id": "LC08_L2SP_146050_20190204_20200829_02_T1",
            "acquisition_date": "2019-02-04T05:22:15Z",
            "spatial_resolution_m": 30.0,
            "cloud_cover_pct": 1.10,
            "bands_used": ["B4 (Red)", "B3 (Green)", "B2 (Blue)", "B5 (NIR)"],
            "verification_status": "SCENE_ID_VERIFIED_RAW_RASTER_OFFLINE",
            "data_provider": "USGS / NASA Earth Observing System"
        },
        "recent_scene": {
            "mission": "USGS/NASA Landsat-9",
            "sensor": "Operational Land Imager 2 (OLI-2)",
            "product_level": "Collection 2 Level-2 Surface Reflectance",
            "scene_id": "LC09_L2SP_146050_20240212_20240213_02_T1",
            "acquisition_date": "2024-02-12T05:22:30Z",
            "spatial_resolution_m": 30.0,
            "cloud_cover_pct": 0.95,
            "bands_used": ["B4 (Red)", "B3 (Green)", "B2 (Blue)", "B5 (NIR)"],
            "verification_status": "SCENE_ID_VERIFIED_RAW_RASTER_OFFLINE",
            "data_provider": "USGS / NASA Earth Observing System"
        },
        "change_analysis": {
            "methodology": "30m Hansen GFC v1.11 stand-replacement loss aggregation",
            "baseline_forest_ha": 820600,
            "detected_canopy_loss_ha": None,
            "reproduction_status": "UNVERIFIED_PENDING_RAW_RASTER_DOWNLOAD",
            "scientific_disclosure": "Scene IDs verified; local bi-temporal pixel subtraction removed until raw rasters are downloaded."
        }
    }
}

def ingest_scenes():
    out_file = os.path.join(OUTPUT_DIR, "forest_satellite_scenes.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(SATELLITE_SCENES_CATALOG, f, indent=2)

    shutil.copy2(out_file, os.path.join(FRONTEND_DATA_DIR, "forest_satellite_scenes.json"))
    print(f"Satellite scenes catalog written to {out_file} (unreproduced loss numbers removed)")

if __name__ == "__main__":
    ingest_scenes()
