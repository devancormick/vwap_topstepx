# VWAP-Based Automated Trading Strategy for TopstepX

A minimal viable product (MVP) VWAP-based automated trading strategy using the TopstepX API (`project-x-py`).

## Overview

This strategy calculates Volume Weighted Average Price (VWAP) from historical market data and places limit orders at VWAP deviation bands for Micro Gold Future (MGC) contracts. Orders are placed on a configurable timer, and the strategy maintains only one trade at a time.

![Architecture Diagram](architecture.png)

## Features

- VWAP calculation from historical market data
- Entry logic at VWAP ± deviation (configurable: 2.0 or 3.0)
- Timer-based order placement (default: every 30 minutes)
- Single position management (one trade at a time)
- Configurable parameters (deviation, timer interval, contract size)

## Prerequisites

1. **TopstepX API Access**: Subscribe to TopstepX API access and obtain your API credentials
2. **Python 3.7+**: Ensure Python is installed on your system
3. **API Credentials**: API key and username from TopstepX

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:

   **Option 1: Using a .env file (recommended for local development)**
   - Copy `.env.example` to `.env`
   - Fill in your TopstepX API credentials in `.env`:
     ```
     PROJECT_X_API_KEY=your_api_key_here
     PROJECT_X_USERNAME=your_username_here
     ```
   
   **Option 2: Set environment variables directly (recommended for production)**
   - Linux/Mac:
     ```bash
     export PROJECT_X_API_KEY=your_api_key_here
     export PROJECT_X_USERNAME=your_username_here
     ```
   - Windows (PowerShell):
     ```powershell
     $env:PROJECT_X_API_KEY="your_api_key_here"
     $env:PROJECT_X_USERNAME="your_username_here"
     ```
   - Windows (CMD):
     ```cmd
     set PROJECT_X_API_KEY=your_api_key_here
     set PROJECT_X_USERNAME=your_username_here
     ```
   
   Note: The `.env` file is optional. If it doesn't exist, the application will use system environment variables.

## Configuration

Edit `config.py` or set environment variables to configure:
- `VWAP_DEVIATION`: Deviation from VWAP for entry points (default: 2.0)
- `TIMER_INTERVAL`: Time interval between order checks in seconds (default: 1800 = 30 minutes)
- `CONTRACT_SIZE`: Number of contracts per trade (default: 1)
- `INSTRUMENT`: Trading instrument symbol (default: 'MGC')

## Usage

Run the strategy:
```bash
python main.py
```

The strategy will:
1. Check for existing open positions
2. Fetch historical market data and calculate VWAP
3. Determine entry points based on VWAP deviation
4. Place limit orders if price conditions are met
5. Repeat on the configured timer interval

Press `Ctrl+C` to stop the strategy gracefully.

## Strategy Logic

![VWAP Trading Strategy](VWAP-Based%20Trading%20Strategy.png)

- **Long Entry**: Place BUY limit order when current price ≤ VWAP - deviation
- **Short Entry**: Place SELL limit order when current price ≥ VWAP + deviation
- **Position Management**: Only one trade at a time; skips order placement if position exists

## Important Notes

- Test thoroughly in a simulated/paper trading environment before live trading
- Ensure compliance with Topstep's terms of use
- Monitor the strategy and implement appropriate risk management
- API method names may need adjustment based on actual `project-x-py` documentation

## Future Trajectory

After successful testing, this MVP could evolve in a prop trading setup through the following enhancements:

### Risk Management
- **Dynamic position sizing**: Implement Kelly Criterion or fixed fractional position sizing based on account equity
- **Stop-loss and take-profit**: Add automated exit logic with trailing stops and profit targets
- **Daily loss limits**: Implement maximum drawdown and daily loss limits to protect capital
- **Volatility-adjusted entries**: Adjust deviation thresholds based on market volatility (ATR, VIX)

### Multi-Instrument & Portfolio Management
- **Multi-symbol support**: Extend strategy to trade multiple instruments simultaneously (ES, NQ, YM, etc.)
- **Correlation analysis**: Implement portfolio-level risk management considering instrument correlations
- **Capital allocation**: Distribute capital across multiple instruments based on Sharpe ratios and market conditions
- **Cross-asset opportunities**: Extend VWAP strategy to other asset classes (forex, crypto, equities)

### Advanced Strategy Features
- **Multiple timeframe analysis**: Incorporate VWAP calculations across different timeframes (15min, 1hr, daily)
- **Volume profile integration**: Combine VWAP with Volume Profile analysis for better entry/exit points
- **Mean reversion filters**: Add additional filters (RSI, Bollinger Bands) to improve entry quality
- **Market regime detection**: Adapt strategy parameters based on trending vs. ranging market conditions

### Performance & Analytics
- **Backtesting framework**: Implement comprehensive backtesting with historical data and performance metrics
- **Real-time monitoring dashboard**: Build web-based dashboard for live P&L, drawdown, win rate, and position monitoring
- **Performance analytics**: Track Sharpe ratio, Sortino ratio, maximum drawdown, and other key metrics
- **Trade journaling**: Log all trades with context for post-analysis and strategy refinement

### Infrastructure & Operations
- **Database integration**: Store trade history, market data, and performance metrics in a database
- **Alerting system**: Implement notifications (email, SMS, Slack) for critical events (large losses, system errors)
- **Deployment automation**: Containerize with Docker and deploy to cloud infrastructure (AWS, GCP)
- **High availability**: Implement redundancy, failover mechanisms, and automatic recovery

### Machine Learning & AI
- **Parameter optimization**: Use ML to optimize VWAP deviation, timer intervals, and position sizing
- **Pattern recognition**: Integrate ML models to identify optimal market conditions for strategy execution
- **Predictive models**: Enhance entry signals with predictive analytics based on market microstructure
- **Adaptive learning**: Implement reinforcement learning to continuously improve strategy performance

### Integration & Scaling
- **Order management system (OMS)**: Integrate with professional OMS for advanced order types and execution
- **Market data feeds**: Upgrade to professional market data providers for lower latency and higher quality data
- **Co-location**: Deploy strategy servers closer to exchange matching engines for reduced latency
- **API rate limiting**: Implement sophisticated rate limiting and order throttling for compliance

This evolution path transforms the MVP from a simple single-instrument strategy into a robust, scalable prop trading system capable of managing multiple strategies and instruments simultaneously while maintaining strict risk controls and performance monitoring.

## License

This is a sample implementation for testing purposes.

