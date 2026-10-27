"""
VARUNA 2047 - Geospatial Analysis Engine Unit Tests
Tests:
- Geometry validity & repair
- Coordinate reference system (CRS) transformation
- NDVI calculation with zero-division handling
- Zonal statistics computation
"""

import os
import sys
import numpy as np
import pytest
from shapely.geometry import Polygon

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from geospatial.vector.boundary import validate_geometry, transform_crs, calculate_centroid
from geospatial.raster.processor import compute_ndvi, create_geotiff, compute_zonal_statistics

def test_validate_geometry_clean():
    coords = [[78.0, 18.0], [79.0, 18.0], [79.0, 19.0], [78.0, 19.0], [78.0, 18.0]]
    poly = Polygon(coords)
    valid_poly = validate_geometry(poly)
    assert valid_poly.is_valid

def test_transform_crs():
    coords = [[78.0, 18.0], [79.0, 18.0], [79.0, 19.0], [78.0, 19.0], [78.0, 18.0]]
    poly = Polygon(coords)
    transformed = transform_crs(poly, "EPSG:4326", "EPSG:3857")
    assert transformed.is_valid
    # Bounds should now be in meters (> 8,000,000 m easting)
    assert transformed.bounds[0] > 1000000

def test_compute_ndvi_values():
    nir = np.array([[0.5, 0.4], [0.3, 0.0]], dtype=np.float32)
    red = np.array([[0.1, 0.4], [0.6, 0.0]], dtype=np.float32)
    ndvi = compute_ndvi(nir, red)

    # (0.5 - 0.1) / (0.5 + 0.1) = 0.4 / 0.6 = ~0.6667 (healthy vegetation)
    assert abs(ndvi[0, 0] - 0.66666) < 0.001
    # (0.4 - 0.4) / (0.4 + 0.4) = 0.0 (bare soil)
    assert abs(ndvi[0, 1] - 0.0) < 0.001
    # (0.3 - 0.6) / (0.3 + 0.6) = -0.3 / 0.9 = -0.3333 (water / cloud)
    assert abs(ndvi[1, 0] - (-0.33333)) < 0.001
    # 0 / 0 handled safely without error or inf
    assert np.isnan(ndvi[1, 1]) or ndvi[1, 1] == -1.0 or abs(ndvi[1, 1]) <= 1.0

def test_zonal_stats_synthetic():
    test_tif = "data/processed/satellite/test_synthetic.tif"
    data = np.ones((10, 10), dtype=np.float32) * 0.45
    bbox = (78.0, 18.0, 79.0, 19.0)
    create_geotiff(data, bbox, output_path=test_tif)

    test_poly = Polygon([[78.2, 18.2], [78.8, 18.2], [78.8, 18.8], [78.2, 18.8], [78.2, 18.2]])
    stats = compute_zonal_statistics(test_tif, test_poly)
    assert stats["count"] > 0
    assert abs(stats["mean"] - 0.45) < 0.01

    if os.path.exists(test_tif):
        os.remove(test_tif)
