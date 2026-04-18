"""
FinPredict FastAPI Application Entry Point
"""
import logging
from fastapi import FastAPI
from api.routes.predict import router as predict_router
from api.routes.health import router as health_router
from api.routes.pipeline import router as pipeline_router
from api.middleware.cors import setup_cors
from monitoring.metrics import setup_metrics
from config import config

logging.basicConfig(
    level=config.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="FinPredict API",
    description="Intelligent Loan Approval Prediction System",
    version="1.0.0"
)

setup_cors(app)
setup_metrics(app)

app.include_router(health_router, tags=["Health"])
app.include_router(predict_router, prefix="/api/v1", tags=["Prediction"])
app.include_router(pipeline_router, prefix="/api/v1", tags=["Pipeline"])

logger.info("FinPredict API started successfully")
