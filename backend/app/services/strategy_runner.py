"""Strategy runner for background execution."""

import time
import logging
from app.services.strategy_service import StrategyService

logger = logging.getLogger(__name__)


def run_strategy_loop(service: StrategyService):
    """Run strategy in a loop until stopped."""
    while service.is_running:
        try:
            if service.strategy:
                service.strategy.execute_strategy()
                time.sleep(service.strategy.timer_interval)
        except Exception as e:
            logger.error(f"Error in strategy execution: {e}")
            service.is_running = False

