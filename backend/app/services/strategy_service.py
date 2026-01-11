"""Strategy service for managing trading strategy."""

import threading
import logging
from typing import Dict, Optional, List
from app.core.config import settings

# Import strategy from parent directory
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from vwap_strategy import VWAPStrategy

logger = logging.getLogger(__name__)


class StrategyService:
    """Service for managing the VWAP trading strategy."""
    
    def __init__(self):
        """Initialize the strategy service."""
        self.strategy: Optional[VWAPStrategy] = None
        self.strategy_thread: Optional[threading.Thread] = None
        self.is_running = False
        self._lock = threading.Lock()
        
    def get_status(self) -> Dict:
        """Get current strategy status."""
        with self._lock:
            return {
                "is_running": self.is_running,
                "status": "running" if self.is_running else "stopped",
                "config": {
                    "vwap_deviation": settings.VWAP_DEVIATION,
                    "timer_interval": settings.TIMER_INTERVAL,
                    "contract_size": settings.CONTRACT_SIZE,
                    "instrument": settings.INSTRUMENT
                }
            }
    
    def start_strategy(self) -> Dict:
        """Start the trading strategy in a background thread."""
        with self._lock:
            if self.is_running:
                return {"status": "already_running", "message": "Strategy is already running"}
            
            try:
                # Initialize strategy
                self.strategy = VWAPStrategy(
                    vwap_deviation=settings.VWAP_DEVIATION,
                    timer_interval=settings.TIMER_INTERVAL,
                    contract_size=settings.CONTRACT_SIZE,
                    instrument=settings.INSTRUMENT
                )
                
                # Start strategy in background thread
                self.strategy_thread = threading.Thread(
                    target=self._run_strategy,
                    daemon=True
                )
                self.strategy_thread.start()
                self.is_running = True
                
                logger.info("Strategy started successfully")
                return {"status": "started", "message": "Strategy started successfully"}
                
            except Exception as e:
                logger.error(f"Error starting strategy: {e}")
                self.is_running = False
                raise
    
    def stop_strategy(self) -> Dict:
        """Stop the trading strategy."""
        with self._lock:
            if not self.is_running:
                return {"status": "already_stopped", "message": "Strategy is not running"}
            
            try:
                self.is_running = False
                # Strategy will stop on next iteration (daemon thread)
                logger.info("Strategy stop requested")
                return {"status": "stopped", "message": "Strategy stop requested"}
                
            except Exception as e:
                logger.error(f"Error stopping strategy: {e}")
                raise
    
    def _run_strategy(self):
        """Internal method to run strategy in background thread."""
        try:
            if self.strategy:
                # Modify strategy to check is_running flag
                while self.is_running:
                    self.strategy.execute_strategy()
                    import time
                    time.sleep(self.strategy.timer_interval)
        except Exception as e:
            logger.error(f"Error in strategy execution: {e}")
            self.is_running = False
    
    def get_positions(self) -> List[Dict]:
        """Get current positions."""
        if not self.strategy:
            return []
        
        try:
            if hasattr(self.strategy, 'has_open_position'):
                has_position = self.strategy.has_open_position()
                return [{"has_position": has_position}] if has_position else []
            return []
        except Exception as e:
            logger.error(f"Error getting positions: {e}")
            return []
    
    def get_vwap_data(self) -> Dict:
        """Get current VWAP calculation data."""
        if not self.strategy:
            return {"error": "Strategy not initialized"}
        
        try:
            # Fetch and calculate VWAP
            data = self.strategy.fetch_market_data()
            vwap = self.strategy.calculate_vwap(data)
            current_price = self.strategy.get_current_price()
            
            return {
                "vwap": vwap,
                "current_price": current_price,
                "deviation": self.strategy.vwap_deviation,
                "long_entry": vwap - self.strategy.vwap_deviation if vwap else None,
                "short_entry": vwap + self.strategy.vwap_deviation if vwap else None,
            }
        except Exception as e:
            logger.error(f"Error getting VWAP data: {e}")
            return {"error": str(e)}

