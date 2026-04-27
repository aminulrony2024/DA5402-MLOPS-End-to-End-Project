"""Prometheus metrics exporter"""
from prometheus_client import Counter, Histogram, Gauge, make_asgi_app
from fastapi import FastAPI

PREDICTION_LATENCY = Histogram(
    "finpredict_prediction_latency_seconds",
    "Time taken for a prediction request"
)

PREDICTION_COUNTER = Counter(
    "finpredict_predictions_total",
    "Total number of prediction requests",
    ["status"]
)

REQUEST_COUNTER = Counter(
    "finpredict_http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint"]
)

# Data drift metric
DATA_DRIFT_SCORE = Gauge(
    "finpredict_data_drift_score",
    "Current data drift score (0=no drift, 1=full drift)"
)


def setup_metrics(app: FastAPI):
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)