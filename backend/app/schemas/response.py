"""
PhishGuard AI - Response Schemas
================================
Pydantic data models for structured API output.
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field


class URLPredictionResponse(BaseModel):
    url: str = Field(..., description="The analyzed URL.")
    prediction: str = Field(..., description="Legitimate or Phishing classification.")
    confidence: float = Field(..., description="Model confidence score between 0.0 and 1.0.")
    risk_level: str = Field(..., description="Risk tier: Low, Moderate, High, or Critical.")
    risk_score: float = Field(..., description="Scaled risk score from 0 to 100.")
    message: str = Field(..., description="Concise human-readable risk summary.")
    analysis_timestamp: str = Field(..., description="ISO 8601 evaluation timestamp.")
    features: Dict[str, Any] = Field(..., description="Dictionary of all 30 extracted features.")
    categories: Dict[str, Any] = Field(..., description="Categorized feature breakdown.")
    detected_risk_flags: List[str] = Field(default_factory=list, description="List of identified suspicious patterns.")
    positive_safety_indicators: List[str] = Field(default_factory=list, description="List of legitimate security signals.")


class HealthResponse(BaseModel):
    status: str = Field(..., json_schema_extra={"example": "healthy"})
    model_loaded: bool = Field(..., json_schema_extra={"example": True})
    supported_features: int = Field(..., json_schema_extra={"example": 30})
    version: str = Field(..., json_schema_extra={"example": "1.0.0"})
    timestamp: str


class ModelInfoResponse(BaseModel):
    model_name: str
    algorithm: str
    num_features: int
    feature_names: List[str]
    classes: List[str]
    best_hyperparameters: Dict[str, Any]
    metrics: Dict[str, Any]
    dataset: Dict[str, Any]
    top_features: List[Dict[str, Any]]
