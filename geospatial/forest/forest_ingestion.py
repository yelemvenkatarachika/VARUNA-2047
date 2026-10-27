"""
VARUNA 2047 - Forest Dataset Ingestion & Harmonization Engine
Loads and harmonizes FSI ISFR assessments and Hansen Global Forest Change time series.
"""

import json
import os
from typing import Dict, Any, List, Optional

class ForestDataIngestion:
    """Ingests and parses state and district forest cover and tree loss data."""

    def __init__(self, data_dir: Optional[str] = None):
        if data_dir is None:
            self.data_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                "data", "processed"
            )
        else:
            self.data_dir = data_dir

    def load_forest_loss_dataset(self) -> Dict[str, Any]:
        """Loads compiled forest loss time-series from data/processed/forest_loss_india.json."""
        filepath = os.path.join(self.data_dir, "forest_loss_india.json")
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Forest loss dataset not found at {filepath}")
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_satellite_scenes_catalog(self) -> Dict[str, Any]:
        """Loads authentic satellite scenes catalog from data/processed/forest_satellite_scenes.json."""
        filepath = os.path.join(self.data_dir, "forest_satellite_scenes.json")
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Satellite scenes catalog not found at {filepath}")
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
