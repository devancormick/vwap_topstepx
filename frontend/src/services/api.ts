import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface StrategyStatus {
  is_running: boolean
  status: string
  config: {
    vwap_deviation: number
    timer_interval: number
    contract_size: number
    instrument: string
  }
}

export interface VWAPData {
  vwap: number | null
  current_price: number | null
  deviation: number
  long_entry: number | null
  short_entry: number | null
}

export const apiService = {
  async getStatus(): Promise<StrategyStatus> {
    const response = await api.get('/api/v1/strategy/status')
    return response.data
  },

  async startStrategy(): Promise<any> {
    const response = await api.post('/api/v1/strategy/control', { action: 'start' })
    return response.data
  },

  async stopStrategy(): Promise<any> {
    const response = await api.post('/api/v1/strategy/control', { action: 'stop' })
    return response.data
  },

  async getVWAP(): Promise<VWAPData> {
    const response = await api.get('/api/v1/strategy/vwap')
    return response.data
  },

  async getPositions(): Promise<any> {
    const response = await api.get('/api/v1/strategy/positions')
    return response.data
  },
}

export default api

