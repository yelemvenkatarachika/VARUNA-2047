"""
VARUNA 2047 - Forest Intelligence Package
Provides research-grade remote sensing, canopy classification, change detection,
zonal aggregation, and scientifically grounded tree-loss estimation for India.
"""

from .provenance import FOREST_PROVENANCE_REGISTRY
from .canopy_classification import CanopyClassifier, DisturbanceType
from .change_detection import ForestChangeDetector
from .zonal_statistics import ZonalForestStatistics
from .forest_metrics import ForestMetricsCalculator
from .tree_count_estimation import TreeCountEstimator

__all__ = [
    "FOREST_PROVENANCE_REGISTRY",
    "CanopyClassifier",
    "DisturbanceType",
    "ForestChangeDetector",
    "ZonalForestStatistics",
    "ForestMetricsCalculator",
    "TreeCountEstimator"
]
