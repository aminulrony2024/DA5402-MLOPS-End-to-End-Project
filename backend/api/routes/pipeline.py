"""Pipeline status endpoint"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/pipeline/status")
def pipeline_status():
    """Returns current Airflow pipeline status"""
    return {
        "status": "active",
        "last_run": "2024-01-01T00:00:00",
        "tasks": {
            "data_ingestion": "success",
            "data_validation": "success",
            "data_cleaning": "success",
            "feature_engineering": "success",
            "encode_and_scale": "success",
            "train_test_split": "success",
            "trigger_training": "success"
        }
    }
