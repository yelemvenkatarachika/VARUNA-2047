"""
VARUNA 2047 - Forest Intelligence Schemas
Defines request and response schemas for forest coverage, change detection,
loss history, satellite comparisons, and evidence reports.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ForestCoverageResponse(BaseModel):
    national_geographical_area_sqkm: float
    national_forest_area_sqkm: float
    national_forest_cover_pct: float
    fsi_assessment_cycle: str
    canopy_distribution: Dict[str, str]
    data_source: str
    states_count: int

class ForestChangeQueryResponse(BaseModel):
    region_id: str
    region_name: str
    region_type: str
    baseline_forest_ha: float
    latest_annual_loss_ha: float
    cumulative_loss_ha: float
    percentage_change: float
    trajectory: str
    trajectory_description: str
    data_confidence: float
    data_source: str
    spatial_resolution: str

class ForestLossHistoryResponse(BaseModel):
    region_id: str
    region_name: str
    units: str
    time_span: str
    history: Dict[str, float]
    provenance: Dict[str, Any]

class ForestCompareRequest(BaseModel):
    region_id: str = Field(..., json_schema_extra={"example": "WAR"})
    baseline_year: Optional[int] = Field(2019, json_schema_extra={"example": 2019})
    recent_year: Optional[int] = Field(2023, json_schema_extra={"example": 2023})
    canopy_class: Optional[str] = Field("OF", json_schema_extra={"example": "OF"})

class ForestCompareResponse(BaseModel):
    region_id: str
    region_name: str
    baseline_year: int
    recent_year: int
    baseline_forest_ha: float
    loss_area_ha: float
    percentage_change: float
    tree_count_available: bool
    estimated_trees_lost: Optional[int]
    uncertainty_range: Optional[Dict[str, Any]]
    scientific_notice: str
    satellite_scene_ids: Dict[str, str]
    reproduction_status: Optional[str] = None
    methodology: Optional[str] = None
    visual_assets: Optional[Dict[str, str]] = None
    provenance: Dict[str, Any]

class ForestReportGenerateRequest(BaseModel):
    region_id: str = Field(..., json_schema_extra={"example": "WAR"})
    region_type: Optional[str] = Field("district", json_schema_extra={"example": "district"})
    include_satellite_comparison: Optional[bool] = Field(True)

class ForestReportGenerateResponse(BaseModel):
    report_id: str
    region_id: str
    region_name: str
    filename: str
    generated_at: str
    download_url: str
    status: str
