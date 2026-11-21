"""
PhishGuard AI - Model Information Route
=======================================
Endpoint to retrieve algorithm details, evaluation metrics, and feature list.
"""

from fastapi import APIRouter, status
from app.schemas.response import ModelInfoResponse
from app.services.prediction_service import prediction_service

router = APIRouter(tags=["Model Info"])


@router.get(
    "/model-info",
    response_model=ModelInfoResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Machine Learning Model Metadata",
    description="Returns training configuration, hyperparameters, test set evaluation metrics, and feature count."
)
async def get_model_information():
    return prediction_service.get_model_info()
