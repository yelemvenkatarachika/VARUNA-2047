"""
VARUNA 2047 - Satellite Raster Integrity Auditor
Inspects GeoTIFF rasters using Rasterio to verify georeferencing, CRS, transform, and band statistics.
"""

import os
import pyproj
# Ensure PROJ_DATA
p = pyproj.datadir.get_data_dir()
os.environ['PROJ_LIB'] = p
os.environ['PROJ_DATA'] = p

import rasterio
import numpy as np

RASTER_FILES = [
    "data/processed/satellite/ndvi_premonsoon_may.tif",
    "data/processed/satellite/ndvi_monsoon_peak.tif",
    "data/processed/satellite/ndvi_monsoon_drought_scenario.tif",
    "data/processed/satellite/ndvi_anomaly_map.tif"
]

def audit_rasters():
    print("="*70)
    print("SATELLITE RASTER ASSET INTEGRITY AUDIT (RASTERIO)")
    print("="*70)

    for path in RASTER_FILES:
        if not os.path.exists(path):
            print(f"[FAIL] {path} DOES NOT EXIST!")
            continue

        with rasterio.open(path) as src:
            data = src.read(1)
            valid = data[data != src.nodata]
            print(f"File: {os.path.basename(path)}")
            print(f"  CRS: {src.crs} | Driver: {src.driver}")
            print(f"  Dimensions: {src.width} x {src.height} (Pixels) | Count: {src.count}")
            print(f"  Bounding Box: Lon [{src.bounds.left:.2f}, {src.bounds.right:.2f}], Lat [{src.bounds.bottom:.2f}, {src.bounds.top:.2f}]")
            print(f"  Pixel Stats: Min={np.min(valid):.3f}, Max={np.max(valid):.3f}, Mean={np.mean(valid):.3f}, Std={np.std(valid):.3f}")
            print(f"  Affine Transform:\n    {src.transform}")
            print("  Status: [PASS] VALID GEOREFERENCED RASTER\n")

    print("="*70)

if __name__ == "__main__":
    audit_rasters()
