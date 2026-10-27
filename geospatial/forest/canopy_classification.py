"""
VARUNA 2047 - Canopy Density & Disturbance Classification
Implements Forest Survey of India (FSI) standards and scientific disturbance
categorization according to international remote sensing protocols.
"""

from enum import Enum
from typing import Dict, Any, Optional

class CanopyDensityClass(str, Enum):
    VDF = "Very Dense Forest"         # Canopy density >= 70%
    MDF = "Moderately Dense Forest"   # Canopy density 40% - 70%
    OF = "Open Forest"                 # Canopy density 10% - 40%
    SCRUB = "Scrub"                   # Canopy density < 10%
    NON_FOREST = "Non-Forest"         # Agriculture, barren, water, urban

class DisturbanceType(str, Enum):
    TREE_COVER_LOSS = "Tree-Cover Loss"
    PERMANENT_DEFORESTATION = "Confirmed Permanent Deforestation"
    TEMPORARY_DISTURBANCE = "Temporary Vegetation Disturbance"
    FOREST_DEGRADATION = "Canopy Thinning / Degradation"
    FIRE_RELATED_LOSS = "Fire-Induced Canopy Scorching"
    SEASONAL_PHENOLOGY = "Seasonal Deciduous Phenology (False Loss)"
    PLANTATION_HARVEST = "Cyclic Plantation Harvesting"

class CanopyClassifier:
    """Classifies canopy density percent into formal FSI density categories."""

    @staticmethod
    def classify_density(density_pct: float) -> CanopyDensityClass:
        if density_pct >= 70.0:
            return CanopyDensityClass.VDF
        elif density_pct >= 40.0:
            return CanopyDensityClass.MDF
        elif density_pct >= 10.0:
            return CanopyDensityClass.OF
        elif density_pct > 0.0:
            return CanopyDensityClass.SCRUB
        return CanopyDensityClass.NON_FOREST

    @staticmethod
    def classify_disturbance(
        ndvi_loss: float,
        pre_fire_nbr: Optional[float] = None,
        post_fire_nbr: Optional[float] = None,
        land_use_conversion: bool = False,
        plantation_zone: bool = False,
        month_of_observation: int = 5
    ) -> Dict[str, Any]:
        """
        Distinguishes genuine permanent deforestation from temporary disturbances,
        plantation clearings, fire scars, or pre-monsoon dry deciduous leaf drop.
        """
        # 1. Check for seasonal deciduous phenology (March-May pre-monsoon leaf senescence)
        if month_of_observation in [3, 4, 5] and not land_use_conversion and ndvi_loss < 0.25:
            return {
                "type": DisturbanceType.SEASONAL_PHENOLOGY,
                "confidence": 0.85,
                "is_deforestation": False,
                "description": "Seasonal dry deciduous canopy shedding; vegetation normally recovers post-monsoon."
            }

        # 2. Check for plantation harvesting in known commercial/agroforestry blocks
        if plantation_zone and not land_use_conversion:
            return {
                "type": DisturbanceType.PLANTATION_HARVEST,
                "confidence": 0.80,
                "is_deforestation": False,
                "description": "Cyclic timber or pulpwood harvesting in agroforestry/social forestry plantation."
            }

        # 3. Check for fire burn scar via delta NBR
        if pre_fire_nbr is not None and post_fire_nbr is not None:
            dnbr = pre_fire_nbr - post_fire_nbr
            if dnbr > 0.27:  # Standard USGS Burn Severity Threshold
                return {
                    "type": DisturbanceType.FIRE_RELATED_LOSS,
                    "confidence": 0.90,
                    "is_deforestation": False,
                    "description": "Wildfire or controlled burn canopy scorching; subject to post-fire natural regeneration."
                }

        # 4. Check for confirmed permanent land-use conversion
        if land_use_conversion:
            return {
                "type": DisturbanceType.PERMANENT_DEFORESTATION,
                "confidence": 0.95,
                "is_deforestation": True,
                "description": "Permanent conversion of forest land to agricultural, mining, or infrastructural use."
            }

        # 5. Stand-replacement canopy loss (Hansen tree-cover loss definition)
        if ndvi_loss >= 0.30:
            return {
                "type": DisturbanceType.TREE_COVER_LOSS,
                "confidence": 0.82,
                "is_deforestation": False,
                "description": "Measured canopy loss (>= 30% reduction). Ground verification required to confirm permanence."
            }

        # 6. Canopy thinning / degradation
        return {
            "type": DisturbanceType.FOREST_DEGRADATION,
            "confidence": 0.75,
            "is_deforestation": False,
            "description": "Partial canopy thinning or lopping; tree crown remains intact."
        }
