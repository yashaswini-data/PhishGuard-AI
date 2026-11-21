"""
PhishGuard AI - Feature Extraction Module
==========================================
Extracts exactly 30 lexical, structural, domain, and statistical features
from a raw URL string without network calls or opening untrusted links.

Categories:
    A. Address Structure (8 features)
    B. Suspicious URL Patterns (7 features)
    C. Domain Characteristics (7 features)
    D. Additional Characteristics (8 features)
Total: 30 Features.
"""

import math
import re
from typing import Dict, List, Tuple, Any
from urllib.parse import urlparse, parse_qs

# Exact 30 features in strict deterministic order
FEATURE_NAMES: List[str] = [
    # A. Address Structure (8)
    "url_length",
    "hostname_length",
    "path_length",
    "count_dots",
    "count_subdomains",
    "count_directories",
    "count_params",
    "has_fragment",
    # B. Suspicious URL Patterns (7)
    "has_ip_address",
    "has_at_symbol",
    "is_shortened",
    "count_suspicious_words",
    "count_hyphens",
    "has_double_slash_redirect",
    "has_consecutive_dots",
    # C. Domain Characteristics (7)
    "is_https",
    "has_suspicious_port",
    "has_numeric_hostname",
    "count_digits_hostname",
    "has_hyphen_in_domain",
    "count_tld_in_subdomain",
    "has_non_ascii",
    # D. Additional Characteristics (8)
    "has_hex_chars",
    "count_encoded_chars",
    "has_query_string",
    "count_special_chars",
    "has_suspicious_extension",
    "digit_ratio",
    "char_entropy",
    "ratio_digits_to_letters",
]

# Feature Category Mapping
FEATURE_CATEGORIES: Dict[str, List[str]] = {
    "Address Structure": [
        "url_length",
        "hostname_length",
        "path_length",
        "count_dots",
        "count_subdomains",
        "count_directories",
        "count_params",
        "has_fragment",
    ],
    "Suspicious URL Patterns": [
        "has_ip_address",
        "has_at_symbol",
        "is_shortened",
        "count_suspicious_words",
        "count_hyphens",
        "has_double_slash_redirect",
        "has_consecutive_dots",
    ],
    "Domain Characteristics": [
        "is_https",
        "has_suspicious_port",
        "has_numeric_hostname",
        "count_digits_hostname",
        "has_hyphen_in_domain",
        "count_tld_in_subdomain",
        "has_non_ascii",
    ],
    "Additional Characteristics": [
        "has_hex_chars",
        "count_encoded_chars",
        "has_query_string",
        "count_special_chars",
        "has_suspicious_extension",
        "digit_ratio",
        "char_entropy",
        "ratio_digits_to_letters",
    ],
}

# Known URL shortener services
SHORTENER_DOMAINS = {
    "bit.ly", "goo.gl", "tinyurl.com", "t.co", "ow.ly", "is.gd",
    "buff.ly", "adf.ly", "bit.do", "mcaf.ee", "rebrand.ly", "cutt.ly",
    "rb.gy", "shorturl.at", "tiny.cc", "tr.im", "v.gd", "clck.ru",
    "qr.net", "1url.com", "vzturl.com", "shorte.st", "po.st"
}

# High-risk phishing target keywords
SUSPICIOUS_KEYWORDS = [
    "login", "verify", "update", "secure", "account", "banking",
    "signin", "confirm", "security", "wallet", "password", "authenticate",
    "auth", "support", "billing", "ebayisapi", "webscr", "appleid",
    "recovery", "credential", "suspend", "validate", "payment"
]

# Suspicious file extensions often associated with drive-by downloads / payloads
SUSPICIOUS_EXTENSIONS = (
    ".exe", ".scr", ".bin", ".apk", ".bat", ".cmd", ".msi",
    ".jar", ".vbs", ".sh", ".php", ".phtml", ".cgi"
)

# Known common TLDs for checking deceptive subdomains (e.g. paypal.com.evil.ru)
COMMON_TLDS = {
    "com", "net", "org", "edu", "gov", "mil", "io", "co", "xyz", "online",
    "info", "biz", "top", "club", "site", "live", "store", "app", "dev"
}

IPV4_PATTERN = re.compile(
    r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}"
    r"(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
)


def calculate_entropy(text: str) -> float:
    """Calculate Shannon entropy (bits per character) of a string."""
    if not text:
        return 0.0
    length = len(text)
    counts: Dict[str, int] = {}
    for char in text:
        counts[char] = counts.get(char, 0) + 1
    entropy = 0.0
    for count in counts.values():
        p = count / length
        entropy -= p * math.log2(p)
    return round(entropy, 4)


def normalize_url(raw_url: str) -> str:
    """Safely normalizes input URL without altering untrusted components."""
    url = raw_url.strip()
    if not url.startswith(("http://", "https://", "ftp://")):
        url = "http://" + url
    return url


def extract_features_dict(raw_url: str) -> Dict[str, Any]:
    """
    Extracts all 30 features from a given URL and returns a dictionary.
    Safe, offline, deterministic.
    """
    normalized_url = normalize_url(raw_url)
    parsed = urlparse(normalized_url)

    url_str = normalized_url
    hostname = (parsed.hostname or "").lower()
    path = parsed.path or ""
    query = parsed.query or ""
    fragment = parsed.fragment or ""
    port = parsed.port

    # --- Category A: Address Structure (8 features) ---
    url_length = len(url_str)
    hostname_length = len(hostname)
    path_length = len(path)
    count_dots = url_str.count(".")

    # Hostname subdomain counting (split by dots, excluding base domain and TLD)
    host_parts = [p for p in hostname.split(".") if p]
    if len(host_parts) > 2:
        count_subdomains = len(host_parts) - 2
    else:
        count_subdomains = 0

    count_directories = path.count("/")
    # Query parameters
    if query:
        count_params = len(parse_qs(query, keep_blank_values=True))
    else:
        count_params = 0
    has_fragment = 1 if fragment else 0

    # --- Category B: Suspicious URL Patterns (7 features) ---
    # IP address check
    has_ip = 1 if IPV4_PATTERN.match(hostname) else 0
    if not has_ip and hostname.replace(".", "").isdigit():
        has_ip = 1

    has_at_symbol = 1 if "@" in url_str else 0

    # Shortened service
    is_shortened = 1 if any(hostname == s or hostname.endswith("." + s) for s in SHORTENER_DOMAINS) else 0

    # Suspicious keywords in hostname or path
    url_lower = url_str.lower()
    count_suspicious_words = sum(1 for kw in SUSPICIOUS_KEYWORDS if kw in url_lower)

    count_hyphens = url_str.count("-")

    # Double slash redirect (in path, e.g. http://legit.com//evil.com or ?u=//evil.com)
    has_double_slash_redirect = 1 if "//" in path else 0

    # Consecutive dots
    has_consecutive_dots = 1 if ".." in url_str else 0

    # --- Category C: Domain Characteristics (7 features) ---
    is_https = 1 if parsed.scheme.lower() == "https" else 0

    # Suspicious port
    if port is not None and port not in (80, 443):
        has_suspicious_port = 1
    else:
        has_suspicious_port = 0

    digits_in_host = sum(1 for c in hostname if c.isdigit())
    has_numeric_hostname = 1 if digits_in_host > 0 else 0
    count_digits_hostname = digits_in_host

    has_hyphen_in_domain = 1 if "-" in hostname else 0

    # Presence of deceptive TLD in subdomain (e.g., paypal.com.attack.ru)
    if len(host_parts) > 2:
        subdomain_tokens = host_parts[:-2]
        count_tld_in_subdomain = 1 if any(token in COMMON_TLDS for token in subdomain_tokens) else 0
    else:
        count_tld_in_subdomain = 0

    # Non-ascii / Punycode (IDN homograph attack)
    has_non_ascii = 1 if ("xn--" in hostname or any(ord(c) > 127 for c in url_str)) else 0

    # --- Category D: Additional Characteristics (8 features) ---
    # Hexadecimal pattern (e.g., 0x41 or %20)
    has_hex = 1 if bool(re.search(r"0x[0-9a-fA-F]+|%[0-9a-fA-F]{2}", url_str)) else 0
    count_encoded_chars = url_str.count("%")
    has_query_string = 1 if bool(query) else 0

    # Special characters
    special_chars = set("~;=_$!*&")
    count_special_chars = sum(1 for c in url_str if c in special_chars)

    # Suspicious file extension
    path_lower = path.lower()
    has_suspicious_extension = 1 if any(path_lower.endswith(ext) for ext in SUSPICIOUS_EXTENSIONS) else 0

    # Digit ratio & character entropy
    total_digits = sum(1 for c in url_str if c.isdigit())
    total_letters = sum(1 for c in url_str if c.isalpha())
    digit_ratio = round(total_digits / (url_length if url_length > 0 else 1), 4)
    char_entropy = calculate_entropy(url_str)
    ratio_digits_to_letters = round(total_digits / (total_letters + 1e-6), 4)

    features = {
        # Category A
        "url_length": int(url_length),
        "hostname_length": int(hostname_length),
        "path_length": int(path_length),
        "count_dots": int(count_dots),
        "count_subdomains": int(count_subdomains),
        "count_directories": int(count_directories),
        "count_params": int(count_params),
        "has_fragment": int(has_fragment),
        # Category B
        "has_ip_address": int(has_ip),
        "has_at_symbol": int(has_at_symbol),
        "is_shortened": int(is_shortened),
        "count_suspicious_words": int(count_suspicious_words),
        "count_hyphens": int(count_hyphens),
        "has_double_slash_redirect": int(has_double_slash_redirect),
        "has_consecutive_dots": int(has_consecutive_dots),
        # Category C
        "is_https": int(is_https),
        "has_suspicious_port": int(has_suspicious_port),
        "has_numeric_hostname": int(has_numeric_hostname),
        "count_digits_hostname": int(count_digits_hostname),
        "has_hyphen_in_domain": int(has_hyphen_in_domain),
        "count_tld_in_subdomain": int(count_tld_in_subdomain),
        "has_non_ascii": int(has_non_ascii),
        # Category D
        "has_hex_chars": int(has_hex),
        "count_encoded_chars": int(count_encoded_chars),
        "has_query_string": int(has_query_string),
        "count_special_chars": int(count_special_chars),
        "has_suspicious_extension": int(has_suspicious_extension),
        "digit_ratio": float(digit_ratio),
        "char_entropy": float(char_entropy),
        "ratio_digits_to_letters": float(ratio_digits_to_letters),
    }

    assert len(features) == 30, f"Expected 30 features, got {len(features)}"
    return features


def extract_features_vector(raw_url: str) -> List[float]:
    """
    Extracts features as a 1D vector strictly matching FEATURE_NAMES order.
    Returns: list of 30 numerical values.
    """
    feat_dict = extract_features_dict(raw_url)
    return [float(feat_dict[name]) for name in FEATURE_NAMES]


def explain_url_features(raw_url: str) -> Dict[str, Any]:
    """
    Returns an interpretable diagnostic breakdown of URL characteristics
    for cybersecurity analysts and end-users.
    """
    feat = extract_features_dict(raw_url)
    flags: List[str] = []
    safeties: List[str] = []

    # Risk signals
    if feat["has_ip_address"] == 1:
        flags.append("Direct IP address used instead of domain name (obfuscation attempt)")
    if feat["has_at_symbol"] == 1:
        flags.append("@ symbol present: browsers ignore preceding credentials, concealing the actual host")
    if feat["is_shortened"] == 1:
        flags.append("URL shortening service detected (conceals true destination)")
    if feat["count_suspicious_words"] > 0:
        flags.append(f"Contains {feat['count_suspicious_words']} sensitive keyword(s) often targeted in credential harvesting")
    if feat["count_hyphens"] >= 3:
        flags.append(f"Excessive hyphens ({feat['count_hyphens']}) detected; often used for typo-squatting or brand impersonation")
    if feat["has_double_slash_redirect"] == 1:
        flags.append("Double slash redirect sequence in path; indicates potential URL redirection evasion")
    if feat["has_consecutive_dots"] == 1:
        flags.append("Consecutive dots ('..') detected; suspicious path traversal or malformed domain structure")
    if feat["is_https"] == 0:
        flags.append("Insecure HTTP protocol used; unencrypted communication channel")
    if feat["has_suspicious_port"] == 1:
        flags.append("Non-standard communication port specified in URL")
    if feat["count_tld_in_subdomain"] == 1:
        flags.append("Deceptive Top-Level Domain embedded inside subdomain (e.g., paypal.com.attack.ru)")
    if feat["has_non_ascii"] == 1:
        flags.append("Punycode or non-ASCII characters detected (possible IDN homograph attack)")
    if feat["has_suspicious_extension"] == 1:
        flags.append("URL path references executable, script, or server payload extension")
    if feat["url_length"] > 75:
        flags.append(f"Unusually long URL ({feat['url_length']} characters); often used to bury malicious payload")

    # Safety signals
    if feat["is_https"] == 1:
        safeties.append("Standard TLS/HTTPS encryption protocol enabled")
    if feat["has_ip_address"] == 0 and feat["is_shortened"] == 0:
        safeties.append("Standard domain name resolution without URL shorteners")
    if feat["count_hyphens"] <= 1 and feat["count_subdomains"] <= 1:
        safeties.append("Clean, unfragmented domain hierarchy")
    if feat["has_suspicious_extension"] == 0:
        safeties.append("No dangerous executable file extension detected")

    # Category summaries
    category_breakdown = {}
    for cat_name, cat_feats in FEATURE_CATEGORIES.items():
        category_breakdown[cat_name] = {k: feat[k] for k in cat_feats}

    return {
        "url": raw_url,
        "features": feat,
        "feature_order": FEATURE_NAMES,
        "categories": category_breakdown,
        "detected_risk_flags": flags,
        "positive_safety_indicators": safeties,
        "total_risk_flags": len(flags)
    }


if __name__ == "__main__":
    # Quick sanity check
    test_url = "https://secure-login.paypal.com.verify-account-update.xyz/login.php?user=admin&token=0x41"
    features = extract_features_dict(test_url)
    print("Features extracted successfully! Count:", len(features))
    explanation = explain_url_features(test_url)
    print("Risk flags detected:", len(explanation["detected_risk_flags"]))
    for flag in explanation["detected_risk_flags"]:
        print(" -", flag)
