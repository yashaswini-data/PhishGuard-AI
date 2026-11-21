"""
PhishGuard AI - Backend Configuration
=====================================
Centralized application settings, CORS, and paths.
"""

import os


class Settings:
    PROJECT_NAME: str = "PhishGuard AI - Intelligent Phishing URL Detection API"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"

    # Paths
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH: str = os.path.join(BASE_DIR, "models", "phishguard_rf_model.joblib")
    METADATA_PATH: str = os.path.join(BASE_DIR, "models", "model_metadata.json")

    # CORS: Allow local development servers
    ALLOWED_ORIGINS: list = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ]


settings = Settings()
