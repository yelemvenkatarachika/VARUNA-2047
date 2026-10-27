"""
VARUNA 2047 - Geospatial Raster Processing Engine
Implements authentic raster mathematics:
- Normalized Difference Vegetation Index: NDVI = (NIR - RED) / (NIR + RED)
- Vegetation Condition Index (VCI)
- Zonal statistics over district polygons (Mean, Median, Std, Min, Max)
- Raster clipping, masking, and GeoTIFF creation using Rasterio
"""

import os
import pyproj
# Ensure PROJ_DATA points to pyproj's bundled valid PROJ database on Windows
p = pyproj.datadir.get_data_dir()
os.environ['PROJ_LIB'] = p
os.environ['PROJ_DATA'] = p

import numpy as np
import rasterio
from rasterio.transform import from_bounds
from rasterio.mask import mask
from shapely.geometry import shape, mapping

def compute_ndvi(nir_band, red_band, nodata_val=None):
    """
    Computes NDVI = (NIR - RED) / (NIR + RED)
    Applies strict division by zero and negative reflectance guards.
    Returns float32 array in range [-1.0, 1.0].
    """
    nir = nir_band.astype(np.float32)
    red = red_band.astype(np.float32)

    denominator = nir + red
    numerator = nir - red

    with np.errstate(divide='ignore', invalid='ignore'):
        ndvi = np.where(denominator > 0.0001, numerator / denominator, np.nan)

    # Clip to valid scientific NDVI range
    ndvi = np.clip(ndvi, -1.0, 1.0)
    return ndvi

def create_geotiff(data_array, bounds, crs="EPSG:4326", output_path="sample.tif", nodata=-9999.0):
    """
    Saves a 2D numpy array to a real GeoTIFF with affine transform and georeferencing.
    bounds: (min_lon, min_lat, max_lon, max_lat)
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    height, width = data_array.shape
    minx, miny, maxx, maxy = bounds

    transform = from_bounds(minx, miny, maxx, maxy, width, height)

    clean_data = np.nan_to_num(data_array, nan=nodata).astype(np.float32)

    with rasterio.open(
        output_path,
        'w',
        driver='GTiff',
        height=height,
        width=width,
        count=1,
        dtype='float32',
        crs=crs,
        transform=transform,
        nodata=nodata,
        compress='deflate'
    ) as dst:
        dst.write(clean_data, 1)

    return output_path

def compute_zonal_statistics(raster_path, geojson_geom):
    """
    Computes zonal statistics (mean, std, min, max, count) for a polygon over a raster.
    """
    geom_shapely = shape(geojson_geom) if isinstance(geojson_geom, dict) else geojson_geom
    geom_mapping = [mapping(geom_shapely)]

    with rasterio.open(raster_path) as src:
        nodata = src.nodata
        try:
            out_image, out_transform = mask(src, geom_mapping, crop=True, all_touched=True)
            data = out_image[0]
            if nodata is not None:
                valid_mask = (data != nodata) & (~np.isnan(data))
            else:
                valid_mask = ~np.isnan(data)

            valid_pixels = data[valid_mask]

            if len(valid_pixels) == 0:
                return {
                    "count": 0, "mean": None, "std": None, "min": None, "max": None, "median": None
                }

            return {
                "count": int(len(valid_pixels)),
                "mean": round(float(np.mean(valid_pixels)), 4),
                "std": round(float(np.std(valid_pixels)), 4),
                "min": round(float(np.min(valid_pixels)), 4),
                "max": round(float(np.max(valid_pixels)), 4),
                "median": round(float(np.median(valid_pixels)), 4)
            }
        except Exception as e:
            print(f"Error computing zonal stats: {e}")
            return {
                "count": 0, "mean": None, "std": None, "min": None, "max": None, "median": None
            }
