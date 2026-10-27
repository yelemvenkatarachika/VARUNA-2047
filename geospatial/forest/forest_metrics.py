"""
VARUNA 2047 - Forest Metrics & Trajectory Calculator
Computes acceleration, decadal comparisons, and regional rankings.
"""

from typing import Dict, Any, List

class ForestMetricsCalculator:
    """Calculates forest dynamics indicators and temporal trajectory."""

    @staticmethod
    def calculate_trajectory(annual_loss_history: Dict[int, float]) -> Dict[str, Any]:
        """
        Calculates trajectory: whether forest loss is accelerating, decelerating, or stable.
        Compares average annual loss of period 1 (e.g. 2011-2017) vs period 2 (2018-2023).
        """
        sorted_years = sorted(annual_loss_history.keys())
        if len(sorted_years) < 4:
            return {
                "trajectory": "INSUFFICIENT_DATA",
                "trajectory_description": "Time series too short to determine trend trajectory.",
                "rate_of_change_pct": 0.0
            }

        mid = len(sorted_years) // 2
        p1_years = sorted_years[:mid]
        p2_years = sorted_years[mid:]

        p1_mean = sum(annual_loss_history[y] for y in p1_years) / len(p1_years)
        p2_mean = sum(annual_loss_history[y] for y in p2_years) / len(p2_years)

        diff = p2_mean - p1_mean
        rate_of_change_pct = (diff / max(1.0, p1_mean)) * 100.0

        if rate_of_change_pct > 15.0:
            status = "ACCELERATING"
            desc = f"Forest loss rate increased by {rate_of_change_pct:.1f}% in the recent period."
        elif rate_of_change_pct < -15.0:
            status = "DECELERATING"
            desc = f"Forest loss rate decreased by {abs(rate_of_change_pct):.1f}% in the recent period."
        else:
            status = "STABLE"
            desc = "Forest loss rate remains within historical baseline bounds (+/- 15%)."

        return {
            "trajectory": status,
            "trajectory_description": desc,
            "period_1_years": f"{p1_years[0]}-{p1_years[-1]}",
            "period_1_mean_ha": round(p1_mean, 2),
            "period_2_years": f"{p2_years[0]}-{p2_years[-1]}",
            "period_2_mean_ha": round(p2_mean, 2),
            "rate_of_change_pct": round(rate_of_change_pct, 2)
        }
