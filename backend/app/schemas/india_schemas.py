"""
VARUNA 2047 - India Administrative & Regional Intelligence Schemas
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class IndiaStateDetail(BaseModel):
    id: str
    name: str
    type: str
    zone: str
    capital: str
    area_sqkm: float
    forest_area_sqkm: float
    forest_cover_pct: float
    fsi_baseline_ha: float
    districts_count: int
    center: List[float]
    bbox: List[float]
    provenance: Dict[str, Any]

class IndiaDistrictDetail(BaseModel):
    id: str
    state_id: str
    name: str
    state: str
    zone: str
    area_sqkm: float
    forest_area_sqkm: float
    forest_cover_pct: float
    fsi_baseline_ha: float
    annual_tree_loss_ha_2023: float
    net_sown_area_ha: float
    major_crops: List[str]
    normal_rainfall_mm: float
    center: List[float]
    provenance: Dict[str, Any]
