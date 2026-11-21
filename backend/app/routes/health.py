"""
PhishGuard AI - Health Check Route
==================================
Endpoint to monitor backend liveness and ML model readiness.
"""

import datetime
from fastapi import APIRouter, status
from app.schemas.response import HealthResponse
from app.services.prediction_service import prediction_service
from config import settings

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Service Health Check",
    description="Returns backend uptime, model loading status, and supported feature count."
)
async def health_check():
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return HealthResponse(
        status="healthy" if prediction_service.is_loaded else "degraded",
        model_loaded=prediction_service.is_loaded,
        supported_features=30,
        version=settings.VERSION,
        timestamp=now_iso
    )
