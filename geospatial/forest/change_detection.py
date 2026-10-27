"""
VARUNA 2047 - Forest Change Detection Engine
Implements multi-temporal raster differencing, quality filtering,
loss pixel identification, and change raster generation.
"""

import numpy as np
from typing import Dict, Any, Tuple, Optional

class ForestChangeDetector:
    """Multi-temporal change detection on raster arrays."""

    @staticmethod
    def compute_ndvi(nir: np.ndarray, red: np.ndarray) -> np.ndarray:
        """Calculates normalized difference vegetation index safely."""
        denominator = nir.astype(float) + red.astype(float)
        denominator[denominator == 0] = 1e-6
        ndvi = (nir.astype(float) - red.astype(float)) / denominator
        return np.clip(ndvi, -1.0, 1.0)

    @staticmethod
    def detect_loss_pixels(
        baseline_ndvi: np.ndarray,
        recent_ndvi: np.ndarray,
        loss_threshold: float = 0.25,
        min_baseline_ndvi: float = 0.40,
        valid_mask: Optional[np.ndarray] = None
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Detects forest-loss pixels where baseline NDVI was dense forest (>= min_baseline_ndvi)
        and declined by at least loss_threshold.
        """
        delta_ndvi = baseline_ndvi - recent_ndvi
        loss_mask = (baseline_ndvi >= min_baseline_ndvi) & (delta_ndvi >= loss_threshold)

        if valid_mask is not None:
            loss_mask = loss_mask & valid_mask

        total_valid = np.sum(valid_mask) if valid_mask is not None else baseline_ndvi.size
        loss_pixels_count = int(np.sum(loss_mask))
        loss_pixel_fraction = float(loss_pixels_count / max(1, total_valid))

        stats = {
            "total_pixels_evaluated": int(total_valid),
            "loss_pixels_count": loss_pixels_count,
            "loss_pixel_fraction": loss_pixel_fraction,
            "mean_delta_ndvi": float(np.mean(delta_ndvi[loss_mask])) if loss_pixels_count > 0 else 0.0,
            "loss_threshold_used": loss_threshold,
            "min_baseline_ndvi_used": min_baseline_ndvi
        }

        return loss_mask, stats

    @staticmethod
    def pixel_to_hectares(pixel_count: int, pixel_resolution_m: float = 30.0) -> float:
        """Converts pixel count at given spatial resolution (in meters) to hectares (1 ha = 10,000 sq m)."""
        area_sq_m = pixel_count * (pixel_resolution_m ** 2)
        return float(area_sq_m / 10000.0)
