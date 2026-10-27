"""
VARUNA 2047 - Core Configuration & Settings
"""

import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "VARUNA 2047"
    PROJECT_TAGLINE: str = "From Global Climate Signals to Local Agricultural Resilience"
    API_V1_STR: str = "/api"
    VERSION: str = "1.0.0"
    
    # Base directory
    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
    DATA_DIR: str = os.path.join(BASE_DIR, "data/processed")
    PROCESSED_DATA_DIR: str = os.path.join(BASE_DIR, "data/processed")
    MODELS_DIR: str = os.path.join(BASE_DIR, "models/saved")
    REPORTS_DIR: str = os.path.join(BASE_DIR, "reports/generated")
    SATELLITE_DIR: str = os.path.join(DATA_DIR, "satellite")
    
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "*"
    ]

    model_config = {"env_file": ".env", "extra": "allow"}

settings = Settings()
