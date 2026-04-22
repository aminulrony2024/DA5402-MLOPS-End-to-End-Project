"""Prometheus metrics exporter"""
from prometheus_client import Counter, Histogram, make_asgi_app
from fastapi import FastAPI
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

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


def setup_metrics(app: FastAPI):
    @app.get("/metrics", include_in_schema=False)
    def metrics():
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
