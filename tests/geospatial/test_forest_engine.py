"""
VARUNA 2047 - Unit Tests for Geospatial Forest Modules
"""

import numpy as np
import pytest
from geospatial.forest.canopy_classification import CanopyClassifier, DisturbanceType, CanopyDensityClass
from geospatial.forest.change_detection import ForestChangeDetector
from geospatial.forest.tree_count_estimation import TreeCountEstimator
from geospatial.forest.zonal_statistics import ZonalForestStatistics
from geospatial.forest.forest_metrics import ForestMetricsCalculator

def test_canopy_classification():
    assert CanopyClassifier.classify_density(85.0) == CanopyDensityClass.VDF
    assert CanopyClassifier.classify_density(55.0) == CanopyDensityClass.MDF
    assert CanopyClassifier.classify_density(25.0) == CanopyDensityClass.OF
    assert CanopyClassifier.classify_density(5.0) == CanopyDensityClass.SCRUB
    assert CanopyClassifier.classify_density(0.0) == CanopyDensityClass.NON_FOREST

def test_disturbance_classification():
    # Seasonal phenology in April
    res = CanopyClassifier.classify_disturbance(ndvi_loss=0.15, month_of_observation=4)
    assert res["type"] == DisturbanceType.SEASONAL_PHENOLOGY
    assert res["is_deforestation"] is False

    # Fire scorch
    res = CanopyClassifier.classify_disturbance(ndvi_loss=0.35, pre_fire_nbr=0.55, post_fire_nbr=0.20)
    assert res["type"] == DisturbanceType.FIRE_RELATED_LOSS

    # Permanent conversion
    res = CanopyClassifier.classify_disturbance(ndvi_loss=0.45, land_use_conversion=True)
    assert res["type"] == DisturbanceType.PERMANENT_DEFORESTATION
    assert res["is_deforestation"] is True

def test_change_detection_engine():
    baseline_ndvi = np.array([
        [0.7, 0.6, 0.2],
        [0.8, 0.5, 0.1],
        [0.75, 0.4, 0.3]
    ])
    recent_ndvi = np.array([
        [0.3, 0.55, 0.2], # (0,0): 0.7 -> 0.3 (loss >= 0.25)
        [0.4, 0.2, 0.1],  # (1,0): 0.8 -> 0.4 (loss >= 0.25), (1,1): 0.5 -> 0.2 (loss >= 0.25)
        [0.7, 0.35, 0.3]
    ])

    loss_mask, stats = ForestChangeDetector.detect_loss_pixels(
        baseline_ndvi=baseline_ndvi,
        recent_ndvi=recent_ndvi,
        loss_threshold=0.25,
        min_baseline_ndvi=0.40
    )

    assert stats["loss_pixels_count"] == 3
    assert loss_mask[0, 0] is np.True_ or loss_mask[0, 0] == True
    assert loss_mask[0, 1] is np.False_ or loss_mask[0, 1] == False

    ha = ForestChangeDetector.pixel_to_hectares(pixel_count=100, pixel_resolution_m=30.0)
    assert ha == 9.0  # 100 * 900 sq m = 90,000 sq m = 9 ha

def test_tree_count_estimation():
    # In accordance with Priority 4, without validated ground forestry plots,
    # spaceborne satellite observations cannot reliably estimate individual tree stems.
    est = TreeCountEstimator.estimate_tree_loss(
        loss_area_ha=10.0,
        baseline_forest_ha=1000.0,
        canopy_class="VDF",
        is_tree_density_defensible=False
    )
    assert est["tree_count_available"] is False
    assert est["estimated_trees_lost"] is None
    assert est["uncertainty_range"] is None
    assert est["loss_area_ha"] == 10.0
    assert est["percentage_change"] == 1.0
    assert "Individual trees lost cannot be reliably determined" in est["scientific_notice"]

def test_zonal_statistics():
    loss_history = {2020: 50.0, 2021: 45.0, 2022: 40.0, 2023: 35.0}
    stats = ZonalForestStatistics.calculate_zonal_loss(
        baseline_forest_ha=10000.0,
        loss_history_ha=loss_history,
        geographic_area_ha=50000.0
    )
    assert stats["cumulative_loss_ha"] == 170.0
    assert stats["percentage_forest_loss"] == 1.7
    assert stats["forest_cover_percentage"] == 20.0
