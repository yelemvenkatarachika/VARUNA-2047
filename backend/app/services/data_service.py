"""
VARUNA 2047 - Data Service
Provides fast in-memory access and querying for authentic ingested datasets.
"""

import os
import json
from datetime import datetime, timezone
from backend.app.core.config import settings

class DataService:
    def __init__(self):
        self._load_datasets()

    def _load_datasets(self):
        # Districts GeoJSON & Metadata
        dist_meta_path = os.path.join(settings.DATA_DIR, "districts_metadata.json")
        dist_geo_path = os.path.join(settings.DATA_DIR, "telangana_districts.geojson")
        
        with open(dist_meta_path, "r", encoding="utf-8") as f:
            self.districts_metadata = json.load(f)
        with open(dist_geo_path, "r", encoding="utf-8") as f:
            self.districts_geojson = json.load(f)

        # ENSO History & Events
        enso_path = os.path.join(settings.DATA_DIR, "enso_history.json")
        events_path = os.path.join(settings.DATA_DIR, "enso_events.json")
        with open(enso_path, "r", encoding="utf-8") as f:
            self.enso_history = json.load(f)
        with open(events_path, "r", encoding="utf-8") as f:
            self.enso_events = json.load(f)

        # Rainfall History
        rf_path = os.path.join(settings.DATA_DIR, "rainfall_history.json")
        with open(rf_path, "r", encoding="utf-8") as f:
            self.rainfall_history = json.load(f)

        # Vegetation History
        veg_path = os.path.join(settings.DATA_DIR, "vegetation_history.json")
        with open(veg_path, "r", encoding="utf-8") as f:
            self.vegetation_history = json.load(f)

        # ISRO & Data Sources Provenance
        isro_path = os.path.join(settings.DATA_DIR, "isro_provenance.json")
        with open(isro_path, "r", encoding="utf-8") as f:
            self.isro_provenance = json.load(f)

    def get_districts(self):
        return {
            "districts": self.districts_metadata,
            "geojson": self.districts_geojson
        }

    def get_district_by_id(self, district_id: str):
        for d in self.districts_metadata:
            if d["id"].upper() == district_id.upper():
                return d
        return None

    def get_enso_history(self):
        return self.enso_history

    def get_current_enso(self):
        latest = self.enso_history["metadata"]["latest_observation"]
        return {
            "latest_observation": latest,
            "provider": self.enso_history["metadata"]["provider"],
            "product": self.enso_history["metadata"]["product_name"],
            "retrieval_timestamp": self.enso_history["metadata"]["retrieval_timestamp"]
        }

    def get_enso_events(self):
        return self.enso_events

    def get_rainfall_history(self, district_id: str = None):
        if district_id:
            summary = self.rainfall_history["district_summaries"].get(district_id.upper())
            return summary
        return self.rainfall_history

    def get_rainfall_anomalies(self, district_id: str = None):
        if district_id:
            summary = self.rainfall_history["district_summaries"].get(district_id.upper())
            if not summary:
                return []
            return [
                {
                    "year": r["year"],
                    "monsoon_jjas_mm": r["monsoon_jjas_mm"],
                    "normal_jjas_mean_mm": r["normal_jjas_mean_mm"],
                    "monsoon_anomaly_pct": r["monsoon_anomaly_pct"],
                    "is_deficit_event": r["is_deficit_event"],
                    "rainfall_category": r["rainfall_category"]
                }
                for r in summary["records"]
            ]
        # Return all districts
        return self.rainfall_history["all_records"]

    def get_satellite_layers(self):
        return {
            "layers": [
                {
                    "id": "isro_bhuvan_wms",
                    "title": "ISRO Bhuvan District Administrative Boundary (Live WMS)",
                    "type": "wms",
                    "source": "ISRO NRSC Bhuvan",
                    "url": "https://bhuvan-vec1.nrsc.gov.in/bhuvan/wms?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&LAYERS=bhuvan:telangana_district_boundary&SRS=EPSG:4326&BBOX=77.5,16.8,81.0,20.2&WIDTH=512&HEIGHT=512&FORMAT=image/png",
                    "active": True,
                    "layer_class": "observational_isro_gis",
                    "attribution": "ISRO / NRSC Bhuvan Geoportal",
                    "description": "Authentic official Telangana district boundaries served via public OGC WMS (HTTP 200)."
                },
                {
                    "id": "isro_sisdp_lulc",
                    "title": "ISRO NRSC SISDP Land Use / Land Cover (Phase-2 WMS)",
                    "type": "wms",
                    "source": "ISRO NRSC SISDP-2",
                    "url": "https://bhuvan-vec1.nrsc.gov.in/bhuvan/wms?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&LAYERS=sisdpv2:TS_Warangal_lulc_v2&SRS=EPSG:4326&BBOX=79.0,17.5,80.5,18.5&WIDTH=512&HEIGHT=512&FORMAT=image/png",
                    "active": True,
                    "layer_class": "observational_isro_thematic",
                    "attribution": "ISRO / NRSC Space Based Information Support for Decentralised Planning (SISDP)",
                    "description": "Authentic ISRO 1:50,000 agricultural and land-cover classification thematic layer."
                },
                {
                    "id": "isro_gw_prospects",
                    "title": "ISRO Ground Water Prospects - Pre-Monsoon (Live WMS)",
                    "type": "wms",
                    "source": "ISRO NRSC RGNDWM",
                    "url": "https://bhuvan-vec1.nrsc.gov.in/bhuvan/wms?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&LAYERS=gw:TELANGANA_PRE&SRS=EPSG:4326&BBOX=77.5,16.8,81.0,20.2&WIDTH=512&HEIGHT=512&FORMAT=image/png",
                    "active": True,
                    "layer_class": "observational_isro_thematic",
                    "attribution": "ISRO / NRSC Rajiv Gandhi National Drinking Water Mission",
                    "description": "Authentic ISRO hydro-geomorphological groundwater prospect mapping."
                },
                {
                    "id": "nasa_gibs_modis",
                    "title": "NASA EOSDIS GIBS MODIS TrueColor (Observational Satellite)",
                    "type": "wmts",
                    "source": "NASA EOSDIS GIBS",
                    "url": "https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/MODIS_Terra_CorrectedReflectance_TrueColor/default/2024-05-15/250m/",
                    "active": True,
                    "layer_class": "observational_satellite",
                    "attribution": "NASA Earth Observing System Data and Information System (EOSDIS)",
                    "description": "Authentic daily 250m satellite true-color corrected surface reflectance."
                },
                {
                    "id": "ndvi_premonsoon_may",
                    "title": "[SIMULATION] Modeled Pre-Monsoon Surface Reflectance (May)",
                    "type": "simulation_raster",
                    "source": "VARUNA Biophysical Simulation Engine",
                    "file": "ndvi_premonsoon_may.tif",
                    "active": False,
                    "bbox": [77.5, 16.8, 81.0, 20.2],
                    "layer_class": "biophysical_simulation",
                    "attribution": "VARUNA Biophysical Simulation Engine (Spatial Demonstration)",
                    "description": "Synthetic mathematical reflectance grid (dry season bare soil & scrub model) generated for spatial engine demonstration. NOT a direct satellite observation."
                },
                {
                    "id": "ndvi_monsoon_peak",
                    "title": "[SIMULATION] Modeled Peak Kharif Canopy Flush (August)",
                    "type": "simulation_raster",
                    "source": "VARUNA Biophysical Simulation Engine",
                    "file": "ndvi_monsoon_peak.tif",
                    "active": False,
                    "bbox": [77.5, 16.8, 81.0, 20.2],
                    "layer_class": "biophysical_simulation",
                    "attribution": "VARUNA Biophysical Simulation Engine (Spatial Demonstration)",
                    "description": "Synthetic mathematical reflectance grid (vigorous vegetative chlorophyll absorption model) generated for spatial engine demonstration. NOT a direct satellite observation."
                },
                {
                    "id": "ndvi_anomaly_map",
                    "title": "[SIMULATION] Modeled Negative Vegetation Anomaly Map",
                    "type": "simulation_raster",
                    "source": "VARUNA Biophysical Simulation Engine",
                    "file": "ndvi_anomaly_map.tif",
                    "active": False,
                    "bbox": [77.5, 16.8, 81.0, 20.2],
                    "layer_class": "biophysical_simulation",
                    "attribution": "VARUNA Biophysical Simulation Engine (Spatial Demonstration)",
                    "description": "Synthetic spatial difference grid demonstrating raster zonal aggregation and deficit visualization."
                }
            ],
            "zonal_statistics": self.vegetation_history.get("zonal_statistics", {})
        }

    def get_satellite_metadata(self):
        return self.vegetation_history.get("metadata", {})

    def get_vegetation_history(self, district_id: str = None):
        records = self.vegetation_history.get("annual_records", [])
        if district_id:
            records = [r for r in records if r["district_id"].upper() == district_id.upper()]
        return {
            "metadata": self.vegetation_history.get("metadata", {}),
            "records": records
        }

    def get_vegetation_anomalies(self, district_id: str = None):
        return self.vegetation_history.get("zonal_statistics", {})

    def get_data_sources_register(self):
        return {
            "provenance_registry": [
                {
                    "source_id": "noaa_cpc_enso",
                    "provider": "NOAA Climate Prediction Center (CPC)",
                    "dataset_name": "Oceanic Niño Index (ONI) - ERSST.v5",
                    "url": "https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt",
                    "status": "Verified Authentic Observational Data (1950-2026, 920 seasons)",
                    "license": "Public Domain (US Government)",
                    "processing": "Monthly timestamp parsing, 3-month running mean, 5-consecutive-season persistence classification"
                },
                {
                    "source_id": "nasa_power_rainfall",
                    "provider": "NASA Langley Research Center",
                    "dataset_name": "NASA POWER Agroclimatology (PRECTOTCORR)",
                    "url": "https://power.larc.nasa.gov/",
                    "status": "Verified Authentic Observational Data (1981-2024, 44 years for 6 Telangana Districts)",
                    "license": "NASA Open Data Policy (Public Domain)",
                    "processing": "Point spatial query, daily-to-monthly total conversion, 1981-2010 reference climatology normal derivation"
                },
                {
                    "source_id": "isro_bhuvan_wms",
                    "provider": "ISRO National Remote Sensing Centre (NRSC)",
                    "dataset_name": "Bhuvan Open Vector Web Map Service (WMS & Thematic LULC / Hydro)",
                    "url": "https://bhuvan-vec1.nrsc.gov.in/bhuvan/wms",
                    "status": "Verified Active (HTTP 200, Official ISRO Thematic & Boundary Layers)",
                    "license": "ISRO Bhuvan Open Web GIS Terms",
                    "processing": "OGC WMS integration for SISDP LULC, Ground Water Prospects, and Telangana district boundaries"
                },
                {
                    "source_id": "varuna_simulation_rasters",
                    "provider": "VARUNA Biophysical Simulation Engine",
                    "dataset_name": "Simulated Deccan Agro-Ecological Reflectance Grids (GeoTIFF)",
                    "url": "Local Engine Generated (data/processed/satellite/)",
                    "status": "Biophysical Plausibility Simulation (Disclosed Synthetic Analog)",
                    "license": "MIT Open Access (Project Generated)",
                    "processing": "Spatial mathematical reflectance modeling, NDVI calculation: (NIR-RED)/(NIR+RED), Rasterio georeferenced GeoTIFF creation, district zonal polygon statistics"
                }
            ],
            "isro_audit": self.isro_provenance
        }

data_service = DataService()
