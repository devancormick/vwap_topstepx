"""Configuration parameters for VWAP trading strategy."""

import os

# VWAP Strategy Parameters (can be overridden by environment variables)
VWAP_DEVIATION = float(os.getenv('VWAP_DEVIATION', '2.0'))  # Deviation from VWAP for entry logic (2.0 or 3.0)
TIMER_INTERVAL = int(os.getenv('TIMER_INTERVAL', '1800'))  # Time interval between order checks in seconds (default: 30 minutes)
CONTRACT_SIZE = int(os.getenv('CONTRACT_SIZE', '1'))  # Fixed contract size per trade
INSTRUMENT = os.getenv('INSTRUMENT', 'MGC')  # Trading instrument (Micro Gold Future)

