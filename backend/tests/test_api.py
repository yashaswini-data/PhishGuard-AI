"""
PhishGuard AI - Comprehensive Backend & API Test Suite
======================================================
Tests URL validation, feature extraction alignment, prediction service,
and FastAPI REST endpoints.
"""

import sys
import os
import pytest
from fastapi.testclient import TestClient

# Ensure backend root is on sys.path
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.main import app
from app.utils.feature_extractor import (
    extract_features_dict,
    extract_features_vector,
    FEATURE_NAMES
)
from app.utils.url_validator import validate_and_sanitize_url

client = TestClient(app)


def test_feature_extractor_30_features():
    """Verify that feature extraction yields exactly 30 features in strict order."""
    url = "https://example.com/login?token=abc#section"
    feats = extract_features_dict(url)
    assert len(feats) == 30, f"Expected 30 features, got {len(feats)}"
    assert list(feats.keys()) == FEATURE_NAMES

    vec = extract_features_vector(url)
    assert len(vec) == 30, f"Expected 30 vector elements, got {len(vec)}"
    assert all(isinstance(v, (int, float)) for v in vec)


def test_url_validation_safe_inputs():
    """Test standard valid URL variations."""
    valid_urls = [
        "https://google.com",
        "http://subdomain.bank.co.uk/portal",
        "github.com/repository/code",
        "https://api.service.io:8443/v1/resource?id=99"
    ]
    for u in valid_urls:
        is_valid, sanitized, err = validate_and_sanitize_url(u)
        assert is_valid is True
        assert sanitized.startswith(("http://", "https://"))
        assert err == ""


def test_url_validation_invalid_inputs():
    """Test rejection of malformed or dangerous inputs."""
    invalid_inputs = [
        "",
        "   ",
        None,
        "http://",
        "https://"
    ]
    for inv in invalid_inputs:
        is_valid, _, err = validate_and_sanitize_url(inv)
        assert is_valid is False
        assert len(err) > 0


def test_health_endpoint():
    """Test GET /health returns 200, healthy status, and 30 features."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True
    assert data["supported_features"] == 30


def test_model_info_endpoint():
    """Test GET /model-info returns Random Forest specs and test metrics."""
    response = client.get("/model-info")
    assert response.status_code == 200
    data = response.json()
    assert data["algorithm"] == "RandomForestClassifier"
    assert data["num_features"] == 30
    assert "metrics" in data
    assert data["metrics"]["accuracy"] > 0.90


def test_predict_legitimate_url():
    """Test POST /predict on a reputable domain."""
    payload = {"url": "https://www.google.com/search?q=cybersecurity+defense"}
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] == "Legitimate"
    assert data["risk_level"] in ("Low", "Moderate")
    assert "features" in data
    assert len(data["features"]) == 30
    assert "categories" in data


def test_predict_phishing_url():
    """Test POST /predict on an obfuscated IP phishing URL."""
    payload = {"url": "http://188.128.111.33/iptv/login.php?update=verify&token=0x41"}
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] == "Phishing"
    assert data["risk_level"] in ("High", "Critical")
    assert len(data["detected_risk_flags"]) > 0


def test_predict_empty_url_validation_error():
    """Test POST /predict rejects empty payload with 422."""
    payload = {"url": ""}
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
