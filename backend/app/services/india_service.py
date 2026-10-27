"""
VARUNA 2047 - India Administrative & Geospatial Service
Manages nationwide state and district boundaries, administrative metadata,
and hierarchical region queries.
"""

import json
import os
from typing import Dict, Any, List, Optional
from backend.app.core.config import settings

class IndiaService:
    def __init__(self):
        self.data_dir = settings.PROCESSED_DATA_DIR
        self._states_geojson = None
        self._districts_geojson = None
        self._metadata = None
        self._load_data()

    def _load_data(self):
        states_path = os.path.join(self.data_dir, "india_states.geojson")
        districts_path = os.path.join(self.data_dir, "india_districts.geojson")
        meta_path = os.path.join(self.data_dir, "india_admin_metadata.json")

        if os.path.exists(states_path):
            with open(states_path, "r", encoding="utf-8") as f:
                self._states_geojson = json.load(f)
        if os.path.exists(districts_path):
            with open(districts_path, "r", encoding="utf-8") as f:
                self._districts_geojson = json.load(f)
        if os.path.exists(meta_path):
            with open(meta_path, "r", encoding="utf-8") as f:
                self._metadata = json.load(f)

    def get_all_states(self) -> Dict[str, Any]:
        """Returns list of all 36 States/UTs with their properties and GeoJSON."""
        states_list = self._metadata.get("states", []) if self._metadata else []
        return {
            "total_states": len(states_list),
            "states": states_list,
            "geojson": self._states_geojson
        }

    def get_state_by_id(self, state_id: str) -> Optional[Dict[str, Any]]:
        """Returns details for a specific state by its 2-letter ID (e.g. AP, TS, MH)."""
        sid = state_id.upper()
        if not self._metadata:
            return None
        for s in self._metadata.get("states", []):
            if s["id"] == sid:
                # Attach feature geometry if available
                feat = None
                if self._states_geojson:
                    for f in self._states_geojson.get("features", []):
                        if f["properties"]["id"] == sid:
                            feat = f
                            break
                return {**s, "feature": feat}
        return None

    def get_districts_for_state(self, state_id: str) -> Dict[str, Any]:
        """Returns available districts for a specific state."""
        sid = state_id.upper()
        if not self._metadata:
            return {"state_id": sid, "districts": [], "geojson": {"type": "FeatureCollection", "features": []}}

        districts = [d for d in self._metadata.get("districts", []) if d["state_id"] == sid]
        features = []
        if self._districts_geojson:
            features = [
                f for f in self._districts_geojson.get("features", [])
                if f["properties"].get("state_id") == sid
            ]

        return {
            "state_id": sid,
            "total_districts": len(districts),
            "districts": districts,
            "geojson": {
                "type": "FeatureCollection",
                "name": f"Districts_{sid}",
                "features": features
            }
        }

    # Alias mapping for core focus districts to 2019 census administrative slugs
    DISTRICT_ALIASES = {
        "WAR": "TS_WARANGAL_RUR",
        "HAN": "TS_WARANGAL_URB",
        "ADI": "TS_ADILABAD",
        "NIZ": "TS_NIZAMABAD",
        "KAR": "TS_KARIMNAGAR",
        "KHA": "TS_KHAMMAM",
        "GAD": "MH_GADCHIROLI",
        "CHA": "MH_CHANDRAPUR",
        "BAL": "MP_BALAGHAT",
        "UKD": "KA_UTTARA_KANN",
        "IDU": "KL_IDUKKI",
        "MAY": "OD_MAYURBHANJ",
        "KAR_AS": "AS_KARBI_ANGLON"
    }

    def get_district_by_id(self, district_id: str) -> Optional[Dict[str, Any]]:
        """Returns detail for a specific district across India with alias support."""
        did = district_id.upper()
        target_id = self.DISTRICT_ALIASES.get(did, did)

        if not self._metadata:
            return None

        matched_district = None
        for d in self._metadata.get("districts", []):
            d_id = d["id"].upper()
            if d_id == target_id or d_id == did:
                matched_district = d
                break

        # Fallback to name search if ID not matched
        if not matched_district:
            for d in self._metadata.get("districts", []):
                if d["name"].upper().replace(" ", "_") == did:
                    matched_district = d
                    break

        if not matched_district:
            return None

        feat = None
        if self._districts_geojson:
            for f in self._districts_geojson.get("features", []):
                fid = f["properties"]["id"].upper()
                if fid == matched_district["id"].upper():
                    feat = f
                    break

        return {**matched_district, "feature": feat}

india_service = IndiaService()
