"""
PhishGuard AI - End-to-End System & Stress Integration Tests
============================================================
Comprehensive test harness covering:
- Diverse legitimate URL variants
- Diverse phishing & evasion patterns
- Edge cases and malformed inputs
- Latency and throughput benchmarks
"""

import sys
import os
import time
import pytest
from fastapi.testclient import TestClient

BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.main import app

client = TestClient(app)


def test_batch_legitimate_urls():
    """Verify high confidence Legitimate classifications on reputable domains."""
    test_urls = [
        "https://www.google.com/search?q=machine+learning+tutorial",
        "https://github.com/torvalds/linux/commits/master",
        "https://en.wikipedia.org/wiki/Computer_science",
        "https://www.cloudflare.com/products/zero-trust/",
        "https://stackoverflow.com/questions/tagged/python",
        "https://docs.python.org/3/library/urllib.parse.html"
    ]
    for url in test_urls:
        resp = client.post("/predict", json={"url": url})
        assert resp.status_code == 200
        data = resp.json()
        assert data["prediction"] == "Legitimate", f"Failed for {url}: got {data['prediction']}"
        assert data["risk_score"] < 50.0


def test_batch_phishing_evasion_urls():
    """Verify detection on malicious patterns without network connection."""
    phishing_cases = [
        "http://192.168.1.100/admin/login.php?update=verify&token=0x99",
        "http://188.128.111.33/iptv/login.php?user=victim&pass=0x12",
        "http://0efbd9f.wcomhost.com/de/banking-postbank/login/privatkunden/de/clients/pass.php"
    ]
    for url in phishing_cases:
        resp = client.post("/predict", json={"url": url})
        assert resp.status_code == 200
        data = resp.json()
        assert data["prediction"] == "Phishing", f"Failed for {url}: got {data['prediction']}"
        assert data["risk_score"] >= 50.0
        assert len(data["detected_risk_flags"]) > 0


def test_edge_cases_and_malformed():
    """Test resilience against edge-case strings."""
    # 1. URL without scheme (auto-prepended with http://)
    resp = client.post("/predict", json={"url": "google.com/search"})
    assert resp.status_code == 200

    # 2. Huge URL within 2048 limit
    huge_url = "https://example.com/path?" + "&".join([f"param{i}={i}" for i in range(50)])
    resp = client.post("/predict", json={"url": huge_url})
    assert resp.status_code == 200

    # 3. URL exceeding 2048 chars
    too_long = "https://example.com/" + "a" * 2100
    resp = client.post("/predict", json={"url": too_long})
    assert resp.status_code == 422

    # 4. Empty and whitespace
    resp = client.post("/predict", json={"url": "   "})
    assert resp.status_code == 422


def test_inference_latency_benchmark():
    """Verify that feature extraction + model prediction executes with high performance."""
    url = "https://secure-login.paypal.com.verify-account-update.xyz/login.php?token=admin"
    latencies = []

    # Warmup
    client.post("/predict", json={"url": url})

    for _ in range(15):
        t0 = time.perf_counter()
        resp = client.post("/predict", json={"url": url})
        t1 = time.perf_counter()
        assert resp.status_code == 200
        latencies.append((t1 - t0) * 1000.0)

    avg_ms = sum(latencies) / len(latencies)
    print(f"\n[Benchmark] Average Inference Latency: {avg_ms:.2f} ms")
    assert avg_ms < 150.0, f"Inference too slow: {avg_ms:.2f} ms"
