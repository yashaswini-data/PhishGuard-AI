"""
PhishGuard AI - URL Validation Utility
======================================
Validates URL syntax safely without making network requests.
"""

import re
from urllib.parse import urlparse
from typing import Tuple


URL_REGEX = re.compile(
    r"^(?:http|ftp)s?://"  # http:// or https:// or ftp://
    r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
    r"localhost|"  # localhost...
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
    r"(?::\d+)?"  # optional port
    r"(?:/?|[/?]\S+)$", re.IGNORECASE
)


def validate_and_sanitize_url(raw_url: str) -> Tuple[bool, str, str]:
    """
    Validates and sanitizes a user-supplied URL.
    Returns:
        (is_valid: bool, sanitized_url: str, error_message: str)
    """
    if not raw_url or not isinstance(raw_url, str):
        return False, "", "URL cannot be empty."

    url = raw_url.strip()

    if len(url) > 2048:
        return False, "", "URL exceeds maximum permitted length of 2048 characters."

    # Prevent command injection / dangerous escape control characters
    if any(ord(c) < 32 for c in url):
        return False, "", "URL contains invalid ASCII control characters."

    # Automatically prepend http:// if scheme is missing
    if not url.startswith(("http://", "https://", "ftp://")):
        url = "http://" + url

    try:
        parsed = urlparse(url)
        if not parsed.netloc:
            return False, "", "Invalid URL: Missing domain or hostname."
    except Exception as e:
        return False, "", f"Malformed URL syntax: {str(e)}"

    return True, url, ""
