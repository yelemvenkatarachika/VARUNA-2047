"""
VARUNA 2047 - Zonal Forest Statistics Engine
Calculates aggregated forest cover, annual tree-cover loss area,
and percentage changes within administrative polygon boundaries.
"""

from typing import Dict, Any, List

class ZonalForestStatistics:
    """Calculates zonal metrics for states, districts, and ecological zones."""

    @staticmethod
    def calculate_zonal_loss(
        baseline_forest_ha: float,
        loss_history_ha: Dict[int, float],
        geographic_area_ha: float
    ) -> Dict[str, Any]:
        """
        Computes formal zonal metrics including cumulative loss, annual loss rates,
        and current retained forest cover.
        """
        cumulative_loss_ha = sum(loss_history_ha.values())
        pct_loss_of_forest = (cumulative_loss_ha / max(1.0, baseline_forest_ha)) * 100.0
        pct_forest_of_geo = (baseline_forest_ha / max(1.0, geographic_area_ha)) * 100.0
        current_forest_ha = max(0.0, baseline_forest_ha - cumulative_loss_ha)

        sorted_years = sorted(loss_history_ha.keys())
        latest_year = sorted_years[-1] if sorted_years else 2023
        latest_loss_ha = loss_history_ha.get(latest_year, 0.0)

        # 5-year trend (e.g. 2019-2023)
        recent_years = [y for y in sorted_years if y >= (latest_year - 4)]
        mean_recent_annual_loss = (
            sum(loss_history_ha[y] for y in recent_years) / len(recent_years)
            if recent_years else latest_loss_ha
        )

        return {
            "geographic_area_ha": geographic_area_ha,
            "baseline_forest_ha": baseline_forest_ha,
            "current_forest_ha": current_forest_ha,
            "cumulative_loss_ha": round(cumulative_loss_ha, 2),
            "percentage_forest_loss": round(pct_loss_of_forest, 3),
            "forest_cover_percentage": round(pct_forest_of_geo, 2),
            "latest_year": latest_year,
            "latest_annual_loss_ha": round(latest_loss_ha, 2),
            "mean_annual_loss_5yr_ha": round(mean_recent_annual_loss, 2),
            "annual_history": {str(k): round(v, 2) for k, v in sorted(loss_history_ha.items())}
        }
