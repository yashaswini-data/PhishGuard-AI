"""
PhishGuard AI - Request Schemas
===============================
Pydantic data models for incoming API payloads.
"""

from pydantic import BaseModel, Field, field_validator


class URLPredictionRequest(BaseModel):
    url: str = Field(
        ...,
        description="The target URL to analyze for phishing threats.",
        json_schema_extra={"example": "https://secure-login.example.com/account/verify"}
    )

    @field_validator("url")
    @classmethod
    def validate_url_not_empty(cls, value: str) -> str:
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("URL string cannot be empty.")
        if len(trimmed) > 2048:
            raise ValueError("URL string length exceeds limit of 2048 characters.")
        return trimmed
