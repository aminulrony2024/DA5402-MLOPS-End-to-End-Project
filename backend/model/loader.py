"""Load model from MLflow registry"""
import logging
import mlflow.xgboost
from config import config

logger = logging.getLogger(__name__)


def load_model():
    """Load the production model from MLflow Model Registry"""
    try:
        mlflow.set_tracking_uri(config.MLFLOW_TRACKING_URI)
        model_uri = f"models:/{config.MODEL_NAME}/{config.MODEL_STAGE}"
        model = mlflow.xgboost.load_model(model_uri)
        logger.info(f"Model loaded from MLflow: {model_uri}")
        return model
    except Exception as e:
        logger.error(f"Failed to load model from MLflow: {e}")
        raise
