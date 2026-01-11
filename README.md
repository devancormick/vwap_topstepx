# VWAP-Based Automated Trading Strategy - Enterprise Production Application

A production-ready VWAP-based automated trading strategy application with REST API backend and React frontend dashboard for TopstepX.

![Architecture Diagram](architecture.png)

## Architecture

This is a full-stack enterprise application with:

- **Backend**: FastAPI REST API (Python)
- **Frontend**: React + TypeScript dashboard
- **Containerization**: Docker & Docker Compose
- **Production Ready**: Proper error handling, logging, and configuration management

## Features

- 🎯 VWAP calculation from historical market data
- 📊 Real-time dashboard for monitoring strategy status
- 🎛️ Web-based controls to start/stop strategy
- 📈 Live VWAP data and entry point visualization
- ⚙️ Configurable parameters via environment variables
- 🐳 Docker containerization for easy deployment
- 🔒 Production-ready security and error handling

## Project Structure

```
vwap_topstepx/
├── backend/                 # FastAPI backend application
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core configuration
│   │   ├── services/       # Business logic services
│   │   └── main.py         # Application entry point
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Backend container
├── frontend/               # React frontend application
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API client
│   │   └── App.tsx         # Main app component
│   ├── package.json        # Node dependencies
│   └── Dockerfile          # Frontend container
├── docker-compose.yml      # Docker Compose configuration
├── vwap_strategy.py        # Core strategy implementation
├── config.py               # Configuration module
└── README.md               # This file
```

## Prerequisites

- **Docker & Docker Compose** (recommended for production)
- **OR** Python 3.11+ and Node.js 18+ for local development
- **TopstepX API Access** with API credentials

## Quick Start with Docker (Recommended)

1. **Clone the repository**

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your TopstepX credentials:
   ```env
   PROJECT_X_API_KEY=your_api_key_here
   PROJECT_X_USERNAME=your_username_here
   ```

3. **Start the application**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Frontend Dashboard: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/api/docs

## Manual Installation

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**
   ```bash
   export PROJECT_X_API_KEY=your_api_key_here
   export PROJECT_X_USERNAME=your_username_here
   ```

5. **Run the backend**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set environment variables** (optional)
   ```bash
   export VITE_API_URL=http://localhost:8000
   ```

4. **Run the frontend**
   ```bash
   npm run dev
   ```

5. **Access the dashboard**
   - Open http://localhost:3000 in your browser

## Configuration

Configuration is managed through environment variables:

### Required Environment Variables

- `PROJECT_X_API_KEY`: TopstepX API key
- `PROJECT_X_USERNAME`: TopstepX username

### Optional Configuration

- `VWAP_DEVIATION`: Deviation from VWAP (default: 2.0)
- `TIMER_INTERVAL`: Order check interval in seconds (default: 1800 = 30 min)
- `CONTRACT_SIZE`: Number of contracts per trade (default: 1)
- `INSTRUMENT`: Trading instrument symbol (default: 'MGC')
- `DEBUG`: Enable debug mode (default: false)
- `HOST`: Backend host (default: 0.0.0.0)
- `PORT`: Backend port (default: 8000)

## API Endpoints

The backend provides the following REST API endpoints:

### Status & Health

- `GET /api/v1/status` - Get API status
- `GET /api/v1/status/health` - Health check
- `GET /health` - Root health check

### Strategy Control

- `GET /api/v1/strategy/status` - Get strategy status
- `POST /api/v1/strategy/control` - Start/stop strategy
  ```json
  {
    "action": "start"  // or "stop"
  }
  ```
- `GET /api/v1/strategy/vwap` - Get current VWAP data
- `GET /api/v1/strategy/positions` - Get current positions

### Configuration

- `GET /api/v1/config` - Get current configuration

### API Documentation

Interactive API documentation is available at:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## Strategy Logic

![VWAP Trading Strategy](VWAP-Based%20Trading%20Strategy.png)

- **Long Entry**: Place BUY limit order when current price ≤ VWAP - deviation
- **Short Entry**: Place SELL limit order when current price ≥ VWAP + deviation
- **Position Management**: Only one trade at a time; skips order placement if position exists

## Production Deployment

### Docker Deployment

The application is containerized and ready for production deployment:

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Cloud Deployment

The application can be deployed to:
- **AWS**: ECS, EKS, or EC2
- **Google Cloud**: Cloud Run, GKE
- **Azure**: Container Instances, AKS
- **DigitalOcean**: App Platform, Droplets

### Environment Setup for Production

1. Set environment variables securely (use secrets management)
2. Configure CORS origins in `backend/app/core/config.py`
3. Enable HTTPS/TLS for production
4. Set up monitoring and logging
5. Configure database for trade history (optional)

## Development

### Running Tests

```bash
# Backend tests (when available)
cd backend
pytest

# Frontend tests (when available)
cd frontend
npm test
```

### Code Structure

- **Backend**: FastAPI with clean architecture
  - `app/api/` - API routes and endpoints
  - `app/services/` - Business logic
  - `app/core/` - Configuration and shared utilities

- **Frontend**: React with TypeScript
  - `src/components/` - React components
  - `src/services/` - API client services

## Important Notes

⚠️ **Production Considerations**

- Test thoroughly in a simulated/paper trading environment before live trading
- Ensure compliance with Topstep's terms of use
- Implement proper risk management and monitoring
- Use secure secrets management for API credentials
- Monitor the application and implement alerting
- API method names may need adjustment based on actual `project-x-py` documentation

## License

This is an enterprise production application for trading purposes.
