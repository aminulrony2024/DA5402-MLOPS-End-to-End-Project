"""CORS middleware configuration"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import config


def setup_cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
