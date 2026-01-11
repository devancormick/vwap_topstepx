"""Strategy control endpoints."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import logging

from app.core.config import settings
from app.services.strategy_service import StrategyService

router = APIRouter()
logger = logging.getLogger(__name__)

# Global strategy service instance
strategy_service = StrategyService()


class StrategyStatusResponse(BaseModel):
    """Strategy status response model."""
    is_running: bool
    status: str
    config: dict


class StrategyControlRequest(BaseModel):
    """Strategy control request model."""
    action: str  # "start" or "stop"


@router.get("/status", response_model=StrategyStatusResponse)
async def get_strategy_status():
    """Get strategy status."""
    try:
        status = strategy_service.get_status()
        return StrategyStatusResponse(
            is_running=status["is_running"],
            status=status["status"],
            config=status["config"]
        )
    except Exception as e:
        logger.error(f"Error getting strategy status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/control")
async def control_strategy(request: StrategyControlRequest):
    """Start or stop the strategy."""
    try:
        if request.action == "start":
            result = strategy_service.start_strategy()
            return JSONResponse({
                "success": True,
                "message": "Strategy started",
                "status": result
            })
        elif request.action == "stop":
            result = strategy_service.stop_strategy()
            return JSONResponse({
                "success": True,
                "message": "Strategy stopped",
                "status": result
            })
        else:
            raise HTTPException(status_code=400, detail="Invalid action. Use 'start' or 'stop'")
    except Exception as e:
        logger.error(f"Error controlling strategy: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/positions")
async def get_positions():
    """Get current positions."""
    try:
        positions = strategy_service.get_positions()
        return JSONResponse({"positions": positions})
    except Exception as e:
        logger.error(f"Error getting positions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/vwap")
async def get_vwap():
    """Get current VWAP calculation."""
    try:
        vwap_data = strategy_service.get_vwap_data()
        return JSONResponse(vwap_data)
    except Exception as e:
        logger.error(f"Error getting VWAP data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

