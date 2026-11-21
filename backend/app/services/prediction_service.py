"""
PhishGuard AI - Prediction Service
==================================
Loads trained Random Forest model and performs real-time URL risk analysis.
"""

import datetime
import json
import os
import joblib
import numpy as np
import pandas as pd

from app.schemas.response import URLPredictionResponse, ModelInfoResponse
from app.utils.feature_extractor import (
    extract_features_dict,
    extract_features_vector,
    explain_url_features,
    FEATURE_NAMES
)
from config import settings


class PredictionService:
    _instance = None

    def __init__(self):
        self.model = None
        self.metadata = {}
        self.is_loaded = False
        self.load_model()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = PredictionService()
        return cls._instance

    def load_model(self):
        """Loads serialized model and training metadata from disk."""
        model_path = settings.MODEL_PATH
        meta_path = settings.METADATA_PATH

        if not os.path.exists(model_path):
            print(f"[!] Warning: Model file not found at {model_path}")
            return

        try:
            self.model = joblib.load(model_path)
            self.is_loaded = True
            print(f"[+] Loaded ML model from: {model_path}")

            if os.path.exists(meta_path):
                with open(meta_path, "r", encoding="utf-8") as f:
                    self.metadata = json.load(f)
                print(f"[+] Loaded model metadata ({len(self.metadata)} keys)")
        except Exception as e:
            print(f"[!] Failed to load model: {e}")
            self.is_loaded = False

    def predict_url(self, raw_url: str) -> URLPredictionResponse:
        """
        Executes end-to-end classification pipeline for an untrusted input URL:
        1. Extracts 30 features locally without visiting or opening the link.
        2. Passes ordered feature DataFrame to Random Forest model.
        3. Derives probability of phishing, confidence, and calibrated risk level.
        4. Synthesizes human-readable risk indicators and safety signals.
        """
        if not self.is_loaded or self.model is None:
            raise RuntimeError("ML model is not loaded. Ensure train_model.py has been executed.")

        # Extract features
        features_vector = extract_features_vector(raw_url)
        explanation = explain_url_features(raw_url)

        # Build DataFrame with explicit feature names matching training
        X_df = pd.DataFrame([features_vector], columns=FEATURE_NAMES)

        # Inference
        probabilities = self.model.predict_proba(X_df)[0]
        # Class 0: Legitimate, Class 1: Phishing
        p_legit = float(probabilities[0])
        p_phish = float(probabilities[1])

        # Prediction decision threshold
        is_phishing = p_phish >= 0.50
        prediction_label = "Phishing" if is_phishing else "Legitimate"
        confidence = round(p_phish if is_phishing else p_legit, 4)

        # Risk scoring (0 - 100)
        risk_score = round(p_phish * 100.0, 1)

        # Risk level tiers
        if risk_score < 20.0:
            risk_level = "Low"
            message = "No strong phishing indicators were detected. The URL structure matches standard legitimate patterns."
        elif risk_score < 50.0:
            risk_level = "Moderate"
            message = "Some unusual structural elements were detected. Exercise routine caution."
        elif risk_score < 80.0:
            risk_level = "High"
            message = "High risk of phishing or deceptive impersonation. Multiple suspicious indicators detected."
        else:
            risk_level = "Critical"
            message = "Critical phishing alert: The URL exhibits high-severity deception patterns (e.g., suspicious keywords, IP hostname, or obfuscation)."

        now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()

        return URLPredictionResponse(
            url=raw_url,
            prediction=prediction_label,
            confidence=confidence,
            risk_level=risk_level,
            risk_score=risk_score,
            message=message,
            analysis_timestamp=now_iso,
            features=explanation["features"],
            categories=explanation["categories"],
            detected_risk_flags=explanation["detected_risk_flags"],
            positive_safety_indicators=explanation["positive_safety_indicators"]
        )

    def get_model_info(self) -> ModelInfoResponse:
        """Returns metadata about the currently deployed model."""
        if not self.metadata:
            return ModelInfoResponse(
                model_name="PhishGuard AI Random Forest",
                algorithm="RandomForestClassifier",
                num_features=len(FEATURE_NAMES),
                feature_names=FEATURE_NAMES,
                classes=["Legitimate", "Phishing"],
                best_hyperparameters={},
                metrics={},
                dataset={},
                top_features=[]
            )

        return ModelInfoResponse(
            model_name=self.metadata.get("model_name", "PhishGuard AI Random Forest"),
            algorithm=self.metadata.get("algorithm", "RandomForestClassifier"),
            num_features=self.metadata.get("num_features", 30),
            feature_names=self.metadata.get("feature_names", FEATURE_NAMES),
            classes=self.metadata.get("classes", ["Legitimate", "Phishing"]),
            best_hyperparameters=self.metadata.get("best_hyperparameters", {}),
            metrics=self.metadata.get("metrics", {}),
            dataset=self.metadata.get("dataset", {}),
            top_features=self.metadata.get("feature_importances", [])[:10]
        )


prediction_service = PredictionService.get_instance()
