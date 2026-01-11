"""VWAP-based automated trading strategy for TopstepX."""

import time
import datetime
import os
import logging
from typing import Optional
import pandas as pd
from project_x_py import ProjectX

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VWAPStrategy:
    """VWAP-based automated trading strategy for TopstepX."""
    
    def __init__(
        self,
        vwap_deviation: float = 2.0,
        timer_interval: int = 1800,  # 30 minutes in seconds
        contract_size: int = 1,
        instrument: str = 'MGC'
    ):
        """
        Initialize the VWAP strategy.
        
        Args:
            vwap_deviation: Deviation from VWAP for entry logic (2.0 or 3.0)
            timer_interval: Time interval between order checks in seconds (default: 1800 = 30 min)
            contract_size: Fixed contract size per trade
            instrument: Trading instrument (default: MGC for Micro Gold Future)
        """
        self.vwap_deviation = vwap_deviation
        self.timer_interval = timer_interval
        self.contract_size = contract_size
        self.instrument = instrument
        
        # Initialize ProjectX client
        api_key = os.getenv('PROJECT_X_API_KEY')
        username = os.getenv('PROJECT_X_USERNAME')
        
        if not api_key or not username:
            raise ValueError(
                "PROJECT_X_API_KEY and PROJECT_X_USERNAME environment variables must be set"
            )
        
        try:
            # Try from_env() method first (common in project-x-py)
            self.client = ProjectX.from_env()
        except (AttributeError, TypeError):
            # Fallback to direct initialization
            self.client = ProjectX(api_key=api_key, username=username)
        
        self.current_order_id: Optional[str] = None
        
        logger.info(f"Strategy initialized: deviation={vwap_deviation}, "
                   f"interval={timer_interval}s, size={contract_size}, instrument={instrument}")
    
    def fetch_market_data(self, lookback_minutes: int = 240) -> pd.DataFrame:
        """
        Fetch historical market data for VWAP calculation.
        
        Args:
            lookback_minutes: Number of minutes of historical data to fetch
            
        Returns:
            DataFrame with market data
        """
        try:
            end_time = datetime.datetime.utcnow()
            start_time = end_time - datetime.timedelta(minutes=lookback_minutes)
            
            # Try different possible method signatures
            try:
                data = self.client.get_historical_data(
                    instrument=self.instrument,
                    start=start_time.isoformat(),
                    end=end_time.isoformat(),
                    interval='1m'
                )
            except (TypeError, AttributeError):
                # Try alternative parameter names
                data = self.client.get_historical_data(
                    symbol=self.instrument,
                    start=start_time,
                    end=end_time,
                    interval='1m'
                )
            
            df = pd.DataFrame(data)
            if df.empty:
                logger.warning("No market data retrieved")
                return df
            
            # Ensure required columns exist
            required_columns = ['open', 'high', 'low', 'close', 'volume']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                logger.error(f"Missing required columns: {missing_columns}")
                return pd.DataFrame()
            
            # Convert timestamp if needed
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            elif df.index.name == 'timestamp' or isinstance(df.index, pd.DatetimeIndex):
                pass  # Already datetime indexed
            else:
                # Try to infer timestamp column
                for col in df.columns:
                    if 'time' in col.lower() or 'date' in col.lower():
                        df['timestamp'] = pd.to_datetime(df[col])
                        break
            
            return df
            
        except Exception as e:
            logger.error(f"Error fetching market data: {e}")
            return pd.DataFrame()
    
    def calculate_vwap(self, data: pd.DataFrame) -> Optional[float]:
        """
        Calculate Volume Weighted Average Price (VWAP).
        
        Args:
            data: DataFrame with OHLCV data
            
        Returns:
            VWAP value or None if calculation fails
        """
        if data.empty or len(data) < 1:
            logger.warning("Insufficient data for VWAP calculation")
            return None
        
        try:
            # Calculate typical price
            data['typical_price'] = (data['high'] + data['low'] + data['close']) / 3.0
            
            # Calculate price * volume
            data['pv'] = data['typical_price'] * data['volume']
            
            # Calculate VWAP
            total_pv = data['pv'].sum()
            total_volume = data['volume'].sum()
            
            if total_volume == 0:
                logger.warning("Total volume is zero, cannot calculate VWAP")
                return None
            
            vwap = total_pv / total_volume
            return float(vwap)
            
        except Exception as e:
            logger.error(f"Error calculating VWAP: {e}")
            return None
    
    def get_current_price(self) -> Optional[float]:
        """
        Get current market price for the instrument.
        
        Returns:
            Current price or None if unavailable
        """
        try:
            market_data = self.client.get_market_data(self.instrument)
            
            # Try different possible keys for price
            price_keys = ['last_price', 'price', 'close', 'last', 'current_price']
            for key in price_keys:
                if key in market_data:
                    return float(market_data[key])
            
            logger.warning("Could not find price in market data")
            return None
            
        except Exception as e:
            logger.error(f"Error getting current price: {e}")
            return None
    
    def has_open_position(self) -> bool:
        """
        Check if there is an open position.
        
        Returns:
            True if open position exists, False otherwise
        """
        try:
            positions = self.client.get_positions()
            if not positions:
                return False
            
            # Check for positions in the target instrument
            for pos in positions:
                instrument_match = pos.get('instrument') == self.instrument or pos.get('symbol') == self.instrument
                quantity = pos.get('quantity', 0) or pos.get('size', 0)
                if instrument_match and quantity != 0:
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking positions: {e}")
            return False
    
    def cancel_all_orders(self):
        """Cancel all open orders for the instrument."""
        try:
            orders = self.client.get_orders(status='OPEN')
            if not orders:
                return
            
            for order in orders:
                instrument_match = (
                    order.get('instrument') == self.instrument or 
                    order.get('symbol') == self.instrument
                )
                if instrument_match:
                    order_id = order.get('id') or order.get('order_id')
                    if order_id:
                        self.client.cancel_order(order_id)
                        logger.info(f"Cancelled order: {order_id}")
                        if order_id == self.current_order_id:
                            self.current_order_id = None
            
        except Exception as e:
            logger.error(f"Error cancelling orders: {e}")
    
    def place_limit_order(self, side: str, price: float) -> bool:
        """
        Place a limit order.
        
        Args:
            side: 'BUY' or 'SELL'
            price: Limit price
            
        Returns:
            True if order placed successfully, False otherwise
        """
        try:
            # Cancel existing orders first
            self.cancel_all_orders()
            
            # Place new order - try different parameter formats
            order_params = {
                'instrument': self.instrument,
                'order_type': 'LIMIT',
                'side': side,
                'quantity': self.contract_size,
                'price': price
            }
            
            try:
                response = self.client.place_order(**order_params)
            except (TypeError, AttributeError):
                # Try alternative parameter names
                order_params_alt = {
                    'symbol': self.instrument,
                    'type': 'LIMIT',
                    'side': side,
                    'quantity': self.contract_size,
                    'price': price,
                    'time_in_force': 'GTC'
                }
                response = self.client.place_order(**order_params_alt)
            
            # Extract order ID from response
            order_id = response.get('id') or response.get('order_id')
            if order_id:
                self.current_order_id = order_id
                logger.info(f"Placed {side} limit order: {order_id} at {price}")
                return True
            else:
                logger.warning(f"Order placed but no ID returned: {response}")
                return False
                
        except Exception as e:
            logger.error(f"Error placing order: {e}")
            return False
    
    def execute_strategy(self):
        """Execute one iteration of the strategy."""
        logger.info("Executing strategy iteration...")
        
        # Check if we already have an open position
        if self.has_open_position():
            logger.info("Open position exists, skipping order placement")
            return
        
        # Fetch market data and calculate VWAP
        data = self.fetch_market_data()
        vwap = self.calculate_vwap(data)
        
        if vwap is None:
            logger.warning("Could not calculate VWAP, skipping iteration")
            return
        
        # Get current price
        current_price = self.get_current_price()
        if current_price is None:
            logger.warning("Could not get current price, skipping iteration")
            return
        
        logger.info(f"VWAP: {vwap:.2f}, Current Price: {current_price:.2f}, "
                   f"Deviation: {self.vwap_deviation}")
        
        # Determine entry logic based on VWAP deviation
        long_entry = vwap - self.vwap_deviation
        short_entry = vwap + self.vwap_deviation
        
        # Place orders based on price relative to VWAP bands
        if current_price <= long_entry:
            logger.info(f"Price below long entry ({long_entry:.2f}), placing BUY order")
            self.place_limit_order('BUY', long_entry)
        elif current_price >= short_entry:
            logger.info(f"Price above short entry ({short_entry:.2f}), placing SELL order")
            self.place_limit_order('SELL', short_entry)
        else:
            logger.info(f"Price within VWAP bands, no action taken")
    
    def run(self):
        """Run the strategy loop."""
        logger.info("Starting VWAP strategy...")
        logger.info(f"Configuration: deviation={self.vwap_deviation}, "
                   f"interval={self.timer_interval}s, size={self.contract_size}")
        
        try:
            while True:
                try:
                    self.execute_strategy()
                except Exception as e:
                    logger.error(f"Error in strategy execution: {e}", exc_info=True)
                
                logger.info(f"Waiting {self.timer_interval} seconds until next check...")
                time.sleep(self.timer_interval)
                
        except KeyboardInterrupt:
            logger.info("Strategy stopped by user")
            self.cancel_all_orders()
        except Exception as e:
            logger.error(f"Strategy error: {e}", exc_info=True)
            self.cancel_all_orders()
            raise

