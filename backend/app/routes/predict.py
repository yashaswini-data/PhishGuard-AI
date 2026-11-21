"""
PhishGuard AI - Prediction Route
================================
Endpoint for submitting untrusted URLs for risk analysis.
"""

from fastapi import APIRouter, HTTPException, status
from app.schemas.request import URLPredictionRequest
from app.schemas.response import URLPredictionResponse
from app.services.prediction_service import prediction_service
from app.utils.url_validator import validate_and_sanitize_url

router = APIRouter(tags=["Prediction"])


@router.post(
    "/predict",
    response_model=URLPredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze and Classify a URL",
    description="Extracts 30 URL features and passes them to the Random Forest model to predict legitimate vs phishing."
)
async def predict_url_endpoint(payload: URLPredictionRequest):
    # 1. Validate and sanitize input without network calls
    is_valid, sanitized_url, error_msg = validate_and_sanitize_url(payload.url)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"URL validation failed: {error_msg}"
        )

    # 2. Run prediction service
    try:
        result = prediction_service.predict_url(sanitized_url)
        return result
    except RuntimeError as re:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(re)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference error processing URL: {str(e)}"
        )
