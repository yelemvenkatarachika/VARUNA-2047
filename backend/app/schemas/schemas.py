"""
VARUNA 2047 - Pydantic Request & Response Schemas
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class HealthResponse(BaseModel):
    status: str
    version: str
    project: str
    datasets_ready: bool
    models_ready: bool
    timestamp: str

class DistrictProperty(BaseModel):
    id: str
    name: str
    state: str
    lat: float
    lon: float
    elevation_m: float
    area_sqkm: float
    agro_climatic_zone: str
    major_crops: List[str]
    normal_monsoon_rainfall_mm: float
    net_sown_area_ha: float
    irrigation_coverage_pct: float

class PredictRiskRequest(BaseModel):
    district_id: str = Field(..., json_schema_extra={"example": "WAR"})
    model_id: Optional[str] = Field("model_b_enso_lr", json_schema_extra={"example": "model_b_enso_lr"})
    nino34_mam: Optional[float] = Field(None, json_schema_extra={"example": 1.2})
    nino34_trend: Optional[float] = Field(None, json_schema_extra={"example": 0.4})
    preseason_mam_rainfall_mm: Optional[float] = Field(None, json_schema_extra={"example": 40.0})
    preseason_may_ndvi: Optional[float] = Field(None, json_schema_extra={"example": 0.24})

class PredictRiskResponse(BaseModel):
    district_id: str
    district_name: str
    model_id: str
    model_name: str
    deficit_probability: float
    risk_level: str
    forecast_issuance_date: str
    primary_drivers: List[Dict[str, Any]]
    confidence_interval: Dict[str, float]
    advisory_recommendation: str

class ResiliencePrioritizeRequest(BaseModel):
    risk_weight: float = Field(0.35, ge=0.0, le=1.0)
    vegetation_stress_weight: float = Field(0.25, ge=0.0, le=1.0)
    exposure_weight: float = Field(0.20, ge=0.0, le=1.0)
    irrigation_vulnerability_weight: float = Field(0.20, ge=0.0, le=1.0)
    year: Optional[int] = Field(2024, json_schema_extra={"example": 2024})

class DistrictPriorityScore(BaseModel):
    district_id: str
    district_name: str
    composite_priority_score: float
    priority_rank: int
    deficit_risk_score: float
    vegetation_stress_score: float
    exposure_score: float
    irrigation_vulnerability_score: float
    primary_vulnerability_factor: str
    suggested_interventions: List[str]

class ResiliencePrioritizeResponse(BaseModel):
    evaluation_year: int
    weight_configuration: Dict[str, float]
    ranked_districts: List[DistrictPriorityScore]
    summary_advisory: str

class GenerateReportRequest(BaseModel):
    district_id: str = Field(..., json_schema_extra={"example": "WAR"})
    year: int = Field(2024, json_schema_extra={"example": 2024})
    include_enso: bool = True
    include_satellite: bool = True
    include_recommendations: bool = True
