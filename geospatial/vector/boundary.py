"""
VARUNA 2047 - Geospatial Vector Module
Handles district boundary validations, CRS transformations, and spatial intersections.
"""

import json
from shapely.geometry import shape, mapping, Polygon, MultiPolygon
from shapely.validation import explain_validity
import pyproj
from pyproj import Transformer

def validate_geometry(geojson_geometry):
    """Checks validity of GeoJSON geometry and repairs minor topological defects if needed."""
    geom = shape(geojson_geometry)
    if not geom.is_valid:
        reason = explain_validity(geom)
        print(f"Warning: Geometry invalid ({reason}). Applying buffer(0)...")
        geom = geom.buffer(0)
    return geom

def calculate_centroid(geom):
    """Returns (lon, lat) of the centroid."""
    c = geom.centroid
    return c.x, c.y

def calculate_bounding_box(geom):
    """Returns (minx, miny, maxx, maxy)."""
    return geom.bounds

def transform_crs(geom, src_crs="EPSG:4326", dst_crs="EPSG:3857"):
    """Transforms a Shapely geometry between coordinate systems."""
    transformer = Transformer.from_crs(src_crs, dst_crs, always_xy=True)
    coords = []
    if geom.geom_type == 'Polygon':
        exterior_coords = [transformer.transform(x, y) for x, y in geom.exterior.coords]
        return Polygon(exterior_coords)
    elif geom.geom_type == 'MultiPolygon':
        polys = []
        for poly in geom.geoms:
            exterior_coords = [transformer.transform(x, y) for x, y in poly.exterior.coords]
            polys.append(Polygon(exterior_coords))
        return MultiPolygon(polys)
    return geom
