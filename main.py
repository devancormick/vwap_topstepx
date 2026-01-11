"""Main entry point for VWAP trading strategy."""

import logging
from dotenv import load_dotenv
import config
from vwap_strategy import VWAPStrategy

# Load environment variables from .env file
load_dotenv()

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

