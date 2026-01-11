"""Status and health check endpoints."""

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.core.config import settings

router = APIRouter()


@router.get("")
async def get_status():
    """Get API status."""
    return JSONResponse({
        "status": "running",
        "version": settings.VERSION,
        "project_name": settings.PROJECT_NAME
    })


@router.get("/health")
async def health():
    """Health check endpoint."""
    return JSONResponse({"status": "healthy"})

