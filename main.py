"""Main entry point for VWAP trading strategy."""

import logging
import config
from vwap_strategy import VWAPStrategy

# Optionally load environment variables from .env file (if it exists)
# Environment variables can also be set directly in the system
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv is optional - environment variables can be set directly
    pass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point."""
    try:
        # Create strategy instance with configuration
        strategy = VWAPStrategy(
            vwap_deviation=config.VWAP_DEVIATION,
            timer_interval=config.TIMER_INTERVAL,
            contract_size=config.CONTRACT_SIZE,
            instrument=config.INSTRUMENT
        )
        
        # Run the strategy
        strategy.run()
        
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        raise


if __name__ == '__main__':
    main()

