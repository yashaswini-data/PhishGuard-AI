"""
PhishGuard AI - Main FastAPI Application
========================================
Production-grade REST API backend for intelligent phishing URL detection.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routes import predict, health, model_info
from app.services.prediction_service import prediction_service
from config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=(
        "Industry-standard machine learning service powered by a Random Forest Classifier "
        "trained on 30 engineered lexical, structural, domain, and statistical URL features. "
        "Evaluates untrusted URLs completely offline without network traversal."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permits local React dev servers on 5173, 3000, etc.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes at both root and /api/v1 prefixes for maximum compatibility
app.include_router(predict.router)
app.include_router(predict.router, prefix=settings.API_PREFIX)

app.include_router(health.router)
app.include_router(health.router, prefix=settings.API_PREFIX)

app.include_router(model_info.router)
app.include_router(model_info.router, prefix=settings.API_PREFIX)


@app.get("/", tags=["Root"])
async def root_index():
    return {
        "project": "PhishGuard AI",
        "description": "Intelligent Phishing URL Detection & Risk Analysis System",
        "version": settings.VERSION,
        "docs": "/docs",
        "health": "/health",
        "status": "online" if prediction_service.is_loaded else "model_missing"
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred during processing.",
            "detail": str(exc),
            "path": str(request.url)
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
