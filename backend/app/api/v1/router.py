"""API v1 router."""

from fastapi import APIRouter

from app.api.v1.endpoints import strategy, status, config

api_router = APIRouter()

api_router.include_router(status.router, prefix="/status", tags=["status"])
api_router.include_router(config.router, prefix="/config", tags=["config"])
api_router.include_router(strategy.router, prefix="/strategy", tags=["strategy"])

