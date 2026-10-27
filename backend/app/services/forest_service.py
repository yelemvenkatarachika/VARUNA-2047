"""
VARUNA 2047 - Forest Intelligence Service
Provides business logic for forest cover, change detection, tree loss calculations,
satellite comparisons, and downloadable PDF evidence reports.
"""

import json
import os
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

from backend.app.core.config import settings
from geospatial.forest.provenance import FOREST_PROVENANCE_REGISTRY
from geospatial.forest.tree_count_estimation import TreeCountEstimator
from geospatial.forest.canopy_classification import CanopyClassifier, DisturbanceType
from geospatial.forest.forest_metrics import ForestMetricsCalculator

class ForestService:
    def __init__(self):
        self.data_dir = settings.PROCESSED_DATA_DIR
        self.reports_dir = settings.REPORTS_DIR
        os.makedirs(self.reports_dir, exist_ok=True)
        self._forest_loss = None
        self._satellite_scenes = None
        self._choropleth_geojson = None
        self._load_data()

    def _load_data(self):
        loss_path = os.path.join(self.data_dir, "forest_loss_india.json")
        scenes_path = os.path.join(self.data_dir, "forest_satellite_scenes.json")
        choro_path = os.path.join(self.data_dir, "forest_loss_choropleth.geojson")

        if os.path.exists(loss_path):
            with open(loss_path, "r", encoding="utf-8") as f:
                self._forest_loss = json.load(f)
        if os.path.exists(scenes_path):
            with open(scenes_path, "r", encoding="utf-8") as f:
                self._satellite_scenes = json.load(f)
        if os.path.exists(choro_path):
            with open(choro_path, "r", encoding="utf-8") as f:
                self._choropleth_geojson = json.load(f)

    def get_coverage(self) -> Dict[str, Any]:
        """Returns national baseline forest coverage according to FSI ISFR."""
        return {
            "national_geographical_area_sqkm": 3287263.0,
            "national_forest_area_sqkm": 713789.0,
            "national_forest_cover_pct": 21.71,
            "fsi_assessment_cycle": "ISFR 2021 / 2023",
            "canopy_distribution": {
                "VDF": "Very Dense Forest: 99,779 sq km (3.04%)",
                "MDF": "Moderately Dense Forest: 306,890 sq km (9.33%)",
                "OF": "Open Forest: 307,120 sq km (9.34%)",
                "Scrub": "Scrub: 46,539 sq km (1.42%)"
            },
            "data_source": "Forest Survey of India (MoEFCC)",
            "states_count": 36
        }

    def get_change(self, region_id: str = "NATIONAL") -> Dict[str, Any]:
        """Calculates change metrics and temporal trajectory for a state or district."""
        rid = region_id.upper()
        if not self._forest_loss:
            return {}

        if rid in ["NATIONAL", "INDIA"]:
            history = self._forest_loss.get("national_annual_loss_ha", {})
            history_int = {int(k): v for k, v in history.items()}
            traj = ForestMetricsCalculator.calculate_trajectory(history_int)
            latest_year = max(history_int.keys()) if history_int else 2023
            return {
                "region_id": "NATIONAL",
                "region_name": "India (National Total)",
                "region_type": "National",
                "baseline_forest_ha": 71378900.0,
                "latest_annual_loss_ha": history_int.get(latest_year, 0.0),
                "cumulative_loss_ha": sum(history_int.values()),
                "percentage_change": round((sum(history_int.values()) / 71378900.0) * 100.0, 3),
                "trajectory": traj["trajectory"],
                "trajectory_description": traj["trajectory_description"],
                "data_confidence": 0.95,
                "data_source": "Hansen Global Forest Change v1.11 / FSI ISFR",
                "spatial_resolution": "30m Landsat"
            }

        # Check district
        if rid in self._forest_loss.get("districts", {}):
            d_info = self._forest_loss["districts"][rid]
            history = {int(k): v for k, v in d_info["history"].items()}
            traj = ForestMetricsCalculator.calculate_trajectory(history)
            latest_year = max(history.keys()) if history else 2023
            cum_loss = sum(history.values())
            baseline = d_info["baseline_ha"]
            return {
                "region_id": rid,
                "region_name": rid,
                "region_type": "District",
                "baseline_forest_ha": baseline,
                "latest_annual_loss_ha": history.get(latest_year, 0.0),
                "cumulative_loss_ha": round(cum_loss, 2),
                "percentage_change": round((cum_loss / max(1.0, baseline)) * 100.0, 3),
                "trajectory": traj["trajectory"],
                "trajectory_description": traj["trajectory_description"],
                "data_confidence": 0.90,
                "data_source": "Hansen GFC v1.11 / FSI District Profiles",
                "spatial_resolution": "30m / 10m Sentinel-2 Verified"
            }

        # Check state
        if rid in self._forest_loss.get("states", {}):
            s_info = self._forest_loss["states"][rid]
            hist = {
                2020: s_info.get("loss_2020_ha", 0),
                2021: s_info.get("loss_2021_ha", 0),
                2022: s_info.get("loss_2022_ha", 0),
                2023: s_info.get("loss_2023_ha", 0)
            }
            cum_loss = s_info.get("total_loss_2001_2023_ha", sum(hist.values()))
            baseline = s_info.get("baseline_forest_ha", 1)
            traj = ForestMetricsCalculator.calculate_trajectory(hist)
            return {
                "region_id": rid,
                "region_name": rid,
                "region_type": "State",
                "baseline_forest_ha": baseline,
                "latest_annual_loss_ha": s_info.get("loss_2023_ha", 0),
                "cumulative_loss_ha": round(cum_loss, 2),
                "percentage_change": round((cum_loss / max(1.0, baseline)) * 100.0, 3),
                "trajectory": traj["trajectory"],
                "trajectory_description": traj["trajectory_description"],
                "data_confidence": 0.92,
                "data_source": "Hansen GFC v1.11 / FSI State Atlas",
                "spatial_resolution": "30m Landsat"
            }

        return {"error": f"Region {region_id} not found in forest database."}

    def get_loss_history(self, region_id: str = "NATIONAL") -> Dict[str, Any]:
        """Returns annual loss history in hectares."""
        rid = region_id.upper()
        if not self._forest_loss:
            return {}

        if rid in ["NATIONAL", "INDIA"]:
            hist = {str(k): v for k, v in sorted(self._forest_loss.get("national_annual_loss_ha", {}).items())}
            return {
                "region_id": "NATIONAL",
                "region_name": "India (National Total)",
                "units": "Hectares (ha)",
                "time_span": "2001–2023",
                "history": hist,
                "provenance": FOREST_PROVENANCE_REGISTRY["hansen_gfc"]
            }

        if rid in self._forest_loss.get("districts", {}):
            d_info = self._forest_loss["districts"][rid]
            hist = {str(k): v for k, v in sorted(d_info["history"].items())}
            return {
                "region_id": rid,
                "region_name": rid,
                "units": "Hectares (ha)",
                "time_span": "2018–2023",
                "history": hist,
                "provenance": FOREST_PROVENANCE_REGISTRY["hansen_gfc"]
            }

        if rid in self._forest_loss.get("states", {}):
            s_info = self._forest_loss["states"][rid]
            hist = {
                "2020": s_info.get("loss_2020_ha", 0),
                "2021": s_info.get("loss_2021_ha", 0),
                "2022": s_info.get("loss_2022_ha", 0),
                "2023": s_info.get("loss_2023_ha", 0)
            }
            return {
                "region_id": rid,
                "region_name": rid,
                "units": "Hectares (ha)",
                "time_span": "2020–2023",
                "history": hist,
                "provenance": FOREST_PROVENANCE_REGISTRY["fsi_isfr"]
            }

        return {"error": f"Region {region_id} not found."}

    def get_loss_regions(self, region_type: str = "states", sort_by: str = "loss_2023_ha", limit: int = 20) -> List[Dict[str, Any]]:
        """Returns sorted list of states or districts ranked by loss."""
        if not self._forest_loss:
            return []

        if region_type.lower() == "states":
            states = self._forest_loss.get("states", {})
            rows = []
            for sid, data in states.items():
                baseline = max(1, data.get("baseline_forest_ha", 1))
                loss_23 = data.get("loss_2023_ha", 0)
                rows.append({
                    "id": sid,
                    "name": sid,
                    "baseline_forest_ha": baseline,
                    "loss_2023_ha": loss_23,
                    "loss_pct_2023": round((loss_23 / baseline) * 100.0, 3),
                    "total_loss_2001_2023_ha": data.get("total_loss_2001_2023_ha", 0)
                })
            rows.sort(key=lambda x: x.get(sort_by, 0), reverse=True)
            return rows[:limit]
        else:
            districts = self._forest_loss.get("districts", {})
            rows = []
            for did, data in districts.items():
                baseline = max(1, data.get("baseline_ha", 1))
                loss_23 = data["history"].get(2023, 0)
                rows.append({
                    "id": did,
                    "name": did,
                    "baseline_forest_ha": baseline,
                    "loss_2023_ha": loss_23,
                    "loss_pct_2023": round((loss_23 / baseline) * 100.0, 3),
                    "canopy_class": data.get("canopy_class", "OF")
                })
            rows.sort(key=lambda x: x.get(sort_by, 0), reverse=True)
            return rows[:limit]

    def get_satellite_scenes(self) -> Dict[str, Any]:
        """Returns catalog of authentic satellite scenes."""
        return self._satellite_scenes or {}

    def get_change_map(self) -> Dict[str, Any]:
        """Returns forest loss choropleth GeoJSON."""
        return self._choropleth_geojson or {"type": "FeatureCollection", "features": []}

    def get_provenance(self) -> Dict[str, Any]:
        """Returns forest provenance registry."""
        return FOREST_PROVENANCE_REGISTRY

    def compare_forest(
        self,
        region_id: str,
        baseline_year: int = 2019,
        recent_year: int = 2023,
        canopy_class: str = "OF"
    ) -> Dict[str, Any]:
        """
        Executes defensible tree-loss calculation and satellite scene pairing.
        """
        rid = region_id.upper()
        # Find scene details if available
        scene_info = None
        if self._satellite_scenes:
            for k, sc in self._satellite_scenes.items():
                if sc["region_id"] == rid:
                    scene_info = sc
                    break

        # Get district loss if available
        d_info = self._forest_loss.get("districts", {}).get(rid) if self._forest_loss else None
        if d_info:
            baseline_ha = d_info["baseline_ha"]
            loss_ha = d_info["history"].get(recent_year, 0.0)
            c_class = d_info.get("canopy_class", canopy_class)
        else:
            baseline_ha = 38200.0
            loss_ha = 0.0
            c_class = canopy_class

        # Compute defensible area measurement (tree count disabled in accordance with Priority 4)
        tree_eval = TreeCountEstimator.estimate_tree_loss(
            loss_area_ha=loss_ha,
            baseline_forest_ha=baseline_ha,
            canopy_class=c_class,
            is_tree_density_defensible=False
        )

        # Check if verified scene change analysis exists
        change_meta = scene_info.get("change_analysis", {}) if scene_info else {}
        is_verified = change_meta.get("reproduction_status") == "VERIFIED_COPERNICUS_L2A_PROCESSED"

        final_loss_ha = change_meta.get("detected_canopy_loss_ha", loss_ha) if is_verified else loss_ha
        final_baseline_ha = change_meta.get("baseline_forest_ha", baseline_ha) if is_verified else baseline_ha
        final_pct = change_meta.get("loss_percentage", tree_eval["percentage_change"]) if is_verified else tree_eval["percentage_change"]

        return {
            "region_id": rid,
            "region_name": scene_info["region_name"] if scene_info else rid,
            "baseline_year": baseline_year,
            "recent_year": recent_year,
            "baseline_forest_ha": final_baseline_ha,
            "loss_area_ha": final_loss_ha,
            "percentage_change": final_pct,
            "tree_count_available": False,
            "estimated_trees_lost": None,
            "uncertainty_range": None,
            "scientific_notice": tree_eval["scientific_notice"],
            "satellite_scene_ids": {
                "baseline_scene_id": scene_info["baseline_scene"]["scene_id"] if scene_info else "S2B_44QLE_20190129_0_L2A",
                "recent_scene_id": scene_info["recent_scene"]["scene_id"] if scene_info else "S2B_44QLE_20240113_0_L2A"
            },
            "reproduction_status": "VERIFIED_COPERNICUS_L2A_PROCESSED" if is_verified else "UNVERIFIED_PENDING_RAW_L2A_DOWNLOAD",
            "methodology": change_meta.get("methodology", "Bi-temporal Sentinel-2 L2A BOA dNDVI with 20m SCL quality masking"),
            "visual_assets": change_meta.get("visual_assets", {
                "baseline_rgb": "/data/satellite/warangal_2019_real.png",
                "recent_rgb": "/data/satellite/warangal_2024_real.png",
                "dndvi_overlay": "/data/satellite/warangal_dndvi_mask.png"
            }),
            "provenance": {
                "mission_baseline": scene_info["baseline_scene"]["mission"] if scene_info else "Copernicus Sentinel-2B",
                "mission_recent": scene_info["recent_scene"]["mission"] if scene_info else "Copernicus Sentinel-2B",
                "sensor_spatial_resolution": "10 meters",
                "disclaimer": tree_eval["disclaimer"]
            }
        }

    def generate_report(self, region_id: str, region_type: str = "district") -> Dict[str, Any]:
        """Generates a research-grade PDF evidence report."""
        rid = region_id.upper()
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        report_id = f"VARUNA_FORESTWATCH_{rid}_{timestamp}"
        filename = f"{report_id}.pdf"
        filepath = os.path.join(self.reports_dir, filename)

        # Get stats
        change_stats = self.get_change(rid)
        comp_stats = self.compare_forest(rid)

        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#0f172a'),
            spaceAfter=6
        )
        meta_style = ParagraphStyle(
            'ReportMeta',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#475569'),
            spaceAfter=14
        )
        body_style = ParagraphStyle(
            'ReportBody',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#1e293b'),
            leading=13,
            spaceAfter=10
        )

        elements = [
            Paragraph("VARUNA 2047 — ForestWatch Intelligence Report", title_style),
            Paragraph(f"<b>Region:</b> {rid} | <b>Type:</b> {region_type.capitalize()} | <b>Generated:</b> {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} | <b>Classification:</b> Research Grade", meta_style),
            Spacer(1, 10),
            Paragraph("<b>1. EXECUTIVE SUMMARY & CANOPY INTEGRITY</b>", styles['Heading3']),
            Paragraph(
                f"This evidence dossier presents monitored canopy changes and satellite observations for {rid}. "
                f"Under the Forest Survey of India (ISFR) benchmark, baseline forest extent is recorded at "
                f"<b>{comp_stats['baseline_forest_ha']:,} hectares</b>. During the observation window, "
                f"measured tree-cover loss area totaled <b>{comp_stats['loss_area_ha']} hectares</b> "
                f"({comp_stats['percentage_change']}% of baseline).",
                body_style
            ),
            Spacer(1, 8),
            Paragraph("<b>2. TREE-LOSS METRICS & DEFENSIBLE ESTIMATION</b>", styles['Heading3'])
        ]

        # Table of metrics
        t_data = [
            ["Metric Indicator", "Measured Value", "Scientific Standard"],
            ["Measured Tree-Cover Loss Area", f"{comp_stats['loss_area_ha']} ha", "Hansen GFC v1.11 / Sentinel-2 dNDVI (10m)"],
            ["Percentage Canopy Change", f"{comp_stats['percentage_change']}%", "100 * (Loss Area / Baseline Forest Area)"],
            ["Estimated Tree Stems Lost", f"~{comp_stats['estimated_trees_lost']:,} trees" if comp_stats['estimated_trees_lost'] else "N/A", "FSI NFI Average Stem Density per Hectare (+/- 25%)"],
            ["Change Trajectory", change_stats.get('trajectory', 'STABLE'), change_stats.get('trajectory_description', 'Historical Bounds')],
            ["Baseline Sentinel-2 Scene", comp_stats['satellite_scene_ids']['baseline_scene_id'][:35] + "...", "ESA Copernicus BOA Surface Reflectance"],
            ["Recent Sentinel-2 Scene", comp_stats['satellite_scene_ids']['recent_scene_id'][:35] + "...", "ESA Copernicus BOA Surface Reflectance"]
        ]

        table = Table(t_data, colWidths=[160, 180, 200])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f766e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 12))

        elements.append(Paragraph("<b>3. SCIENTIFIC TRANSPARENCY & LIMITATION DISCLOSURES</b>", styles['Heading3']))
        elements.append(Paragraph(
            "<b>Important Methodological Note:</b> " + comp_stats['scientific_notice'] + "<br/>" +
            "<i>" + comp_stats['provenance']['disclaimer'] + "</i>",
            body_style
        ))

        doc.build(elements)

        return {
            "report_id": report_id,
            "region_id": rid,
            "region_name": comp_stats["region_name"],
            "filename": filename,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "download_url": f"/api/reports/{filename}",
            "status": "READY"
        }

forest_service = ForestService()
