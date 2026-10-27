"""
VARUNA 2047 - Resilience Prioritization Service
Transparent Multi-Criteria Decision Analysis (MCDA) combining:
1. Validated Seasonal Deficit Probability (from ML Model)
2. Observed Satellite Vegetation Stress (from Sentinel-2 / MODIS VCI)
3. Net Sown Agricultural Exposure (Hectares)
4. Irrigation Vulnerability (100% - Irrigation Coverage %)

Permits adjustable scoring weights with mathematical normalization.
Produces structured, transparent intervention categories.
"""

from typing import Dict, Any, List
from backend.app.services.data_service import data_service
from backend.app.services.model_service import model_service

class ResilienceService:
    def prioritize_districts(
        self,
        risk_weight: float = 0.35,
        veg_stress_weight: float = 0.25,
        exposure_weight: float = 0.20,
        irrigation_weight: float = 0.20,
        year: int = 2024
    ) -> Dict[str, Any]:
        # Normalize weights so sum equals 1.0
        total_w = risk_weight + veg_stress_weight + exposure_weight + irrigation_weight
        if total_w <= 0:
            risk_w, veg_w, exp_w, irr_w = 0.35, 0.25, 0.20, 0.20
        else:
            risk_w = risk_weight / total_w
            veg_w = veg_stress_weight / total_w
            exp_w = exposure_weight / total_w
            irr_w = irrigation_weight / total_w

        districts = data_service.districts_metadata
        scored_districts = []

        max_net_sown = max(d["net_sown_area_ha"] for d in districts)

        for d in districts:
            # 1. Deficit Risk Score (from validated ML model)
            pred = model_service.predict_risk(d)
            deficit_prob = pred["deficit_probability"]
            risk_score = round(deficit_prob * 100.0, 1)

            # 2. Vegetation Stress Score: Inverted VCI (100 - VCI)
            veg_history = data_service.get_vegetation_history(d["id"])["records"]
            yr_veg = [r for r in veg_history if r["year"] == year]
            vci = yr_veg[0]["vci_index"] if yr_veg else 50.0
            veg_stress_score = round(max(0.0, min(100.0, 100.0 - vci)), 1)

            # 3. Agricultural Exposure Score (Normalized Net Sown Area 0-100)
            exposure_score = round((d["net_sown_area_ha"] / max_net_sown) * 100.0, 1)

            # 4. Irrigation Vulnerability Score (100% - Irrigation %)
            irrigation_vuln_score = round(100.0 - d["irrigation_coverage_pct"], 1)

            # Composite Priority Score (0 to 100)
            composite_score = round(
                (risk_w * risk_score) +
                (veg_w * veg_stress_score) +
                (exp_w * exposure_score) +
                (irr_w * irrigation_vuln_score),
                1
            )

            # Determine dominant vulnerability factor
            factor_scores = {
                "Rainfall Deficit Risk": risk_score * risk_w,
                "Vegetation Canopy Stress": veg_stress_score * veg_w,
                "High Rainfed Acreage Exposure": exposure_score * exp_w,
                "Low Irrigation Coverage": irrigation_vuln_score * irr_w
            }
            dominant_factor = max(factor_scores, key=factor_scores.get)

            # Evidence-based intervention suggestions
            interventions = []
            if irrigation_vuln_score >= 60.0:
                interventions.append("Rainfed Micro-Irrigation & Farm Pond Audit")
            if risk_score >= 35.0:
                interventions.append("Pre-Monsoon Contingency Crop Extension Outreach")
            if veg_stress_score >= 45.0:
                interventions.append("Rapid Ground-Truthing & Soil Moisture Field Verification")
            if d["area_sqkm"] > 3500:
                interventions.append("Sub-District Mandal-Level Drought Vulnerability Monitoring")
            interventions.append("Reservoir & Minor Irrigation Tank Level Review")

            scored_districts.append({
                "district_id": d["id"],
                "district_name": d["name"],
                "composite_priority_score": composite_score,
                "deficit_risk_score": risk_score,
                "vegetation_stress_score": veg_stress_score,
                "exposure_score": exposure_score,
                "irrigation_vulnerability_score": irrigation_vuln_score,
                "primary_vulnerability_factor": dominant_factor,
                "suggested_interventions": interventions[:4]
            })

        # Sort by composite priority score descending
        scored_districts.sort(key=lambda x: x["composite_priority_score"], reverse=True)
        for idx, item in enumerate(scored_districts):
            item["priority_rank"] = idx + 1

        return {
            "evaluation_year": year,
            "weight_configuration": {
                "risk_weight": round(risk_w, 3),
                "vegetation_stress_weight": round(veg_w, 3),
                "exposure_weight": round(exp_w, 3),
                "irrigation_vulnerability_weight": round(irr_w, 3)
            },
            "ranked_districts": scored_districts,
            "summary_advisory": (
                f"Districts ranked under {year} pre-monsoon criteria. "
                f"Top priority district is {scored_districts[0]['district_name']} "
                f"(Score: {scored_districts[0]['composite_priority_score']}/100) primarily driven by {scored_districts[0]['primary_vulnerability_factor']}."
            )
        }

resilience_service = ResilienceService()
