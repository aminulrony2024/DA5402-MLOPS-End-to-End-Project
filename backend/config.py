import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", 8000))
    MLFLOW_TRACKING_URI: str = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "FinPredict_XGBoost")
    MODEL_STAGE: str = os.getenv("MODEL_STAGE", "Production")
    ALLOWED_ORIGINS: list = ["http://localhost:3000", "http://127.0.0.1:3000"]
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/app.log")

config = Config()
