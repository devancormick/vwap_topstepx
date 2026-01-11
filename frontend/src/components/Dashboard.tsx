import { useState, useEffect } from 'react'
import { apiService, StrategyStatus, VWAPData } from '../services/api'
import './Dashboard.css'

export default function Dashboard() {
  const [status, setStatus] = useState<StrategyStatus | null>(null)
  const [vwapData, setVWAPData] = useState<VWAPData | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchStatus = async () => {
    try {
      const data = await apiService.getStatus()
      setStatus(data)
    } catch (err: any) {
      setError(err.message || 'Failed to fetch status')
    }
  }

  const fetchVWAP = async () => {
    try {
      const data = await apiService.getVWAP()
      setVWAPData(data)
    } catch (err: any) {
      console.error('Error fetching VWAP:', err)
    }
  }

  useEffect(() => {
    fetchStatus()
    fetchVWAP()
    const interval = setInterval(() => {
      fetchStatus()
      fetchVWAP()
    }, 5000) // Update every 5 seconds
    return () => clearInterval(interval)
  }, [])

  const handleStart = async () => {
    setLoading(true)
    setError(null)
    try {
      await apiService.startStrategy()
      await fetchStatus()
    } catch (err: any) {
      setError(err.message || 'Failed to start strategy')
    } finally {
      setLoading(false)
    }
  }

  const handleStop = async () => {
    setLoading(true)
    setError(null)
    try {
      await apiService.stopStrategy()
      await fetchStatus()
    } catch (err: any) {
      setError(err.message || 'Failed to stop strategy')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>VWAP Trading Strategy Dashboard</h1>
      </header>

      <main className="dashboard-content">
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        <div className="status-card">
          <h2>Strategy Status</h2>
          {status && (
            <div className="status-info">
              <div className={`status-badge ${status.is_running ? 'running' : 'stopped'}`}>
                {status.is_running ? 'Running' : 'Stopped'}
              </div>
              <div className="status-controls">
                <button
                  onClick={handleStart}
                  disabled={loading || status.is_running}
                  className="btn btn-start"
                >
                  Start Strategy
                </button>
                <button
                  onClick={handleStop}
                  disabled={loading || !status.is_running}
                  className="btn btn-stop"
                >
                  Stop Strategy
                </button>
              </div>
            </div>
          )}
        </div>

        {status && (
          <div className="config-card">
            <h2>Configuration</h2>
            <div className="config-grid">
              <div className="config-item">
                <label>VWAP Deviation</label>
                <span>{status.config.vwap_deviation}</span>
              </div>
              <div className="config-item">
                <label>Timer Interval</label>
                <span>{status.config.timer_interval}s ({Math.round(status.config.timer_interval / 60)}min)</span>
              </div>
              <div className="config-item">
                <label>Contract Size</label>
                <span>{status.config.contract_size}</span>
              </div>
              <div className="config-item">
                <label>Instrument</label>
                <span>{status.config.instrument}</span>
              </div>
            </div>
          </div>
        )}

        {vwapData && vwapData.vwap && (
          <div className="vwap-card">
            <h2>VWAP Data</h2>
            <div className="vwap-grid">
              <div className="vwap-item">
                <label>Current VWAP</label>
                <span className="value">{vwapData.vwap.toFixed(2)}</span>
              </div>
              <div className="vwap-item">
                <label>Current Price</label>
                <span className="value">{vwapData.current_price?.toFixed(2) || 'N/A'}</span>
              </div>
              <div className="vwap-item">
                <label>Long Entry</label>
                <span className="value long">{vwapData.long_entry?.toFixed(2) || 'N/A'}</span>
              </div>
              <div className="vwap-item">
                <label>Short Entry</label>
                <span className="value short">{vwapData.short_entry?.toFixed(2) || 'N/A'}</span>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

