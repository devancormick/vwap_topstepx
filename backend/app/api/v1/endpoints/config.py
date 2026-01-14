"""Configuration endpoints."""

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.core.config import settings

router = APIRouter()


class ConfigResponse(BaseModel):
    """Configuration response model."""
    vwap_deviation: float
    timer_interval: int
    contract_size: int
    instrument: str


@router.get("", response_model=ConfigResponse)
async def get_config():
    """Get current configuration."""
    return ConfigResponse(
        vwap_deviation=settings.VWAP_DEVIATION,
        timer_interval=settings.TIMER_INTERVAL,
        contract_size=settings.CONTRACT_SIZE,
        instrument=settings.INSTRUMENT
    )

