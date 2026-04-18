"""Health check endpoints"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health():
    """Liveness check"""
    return {"status": "healthy"}


@router.get("/ready")
def ready():
    """Readiness check"""
    return {"status": "ready", "model": "FinPredict_XGBoost", "version": "1.0.0"}
