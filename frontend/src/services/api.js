import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';
const WS_URL = 'ws://localhost:8000/ws';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Equipment API
export const equipmentAPI = {
  getAll: () => api.get('/equipment'),
  getDashboard: () => api.get('/equipment/dashboard'),
  getStats: () => api.get('/equipment/stats'),
  getById: (id) => api.get(`/equipment/${id}`),
  getReadings: (id, sensorType = null, hours = 24) => {
    const params = { hours };
    if (sensorType) params.sensor_type = sensorType;
    return api.get(`/equipment/${id}/readings`, { params });
  },
  create: (data) => api.post('/equipment', data),
  update: (id, data) => api.patch(`/equipment/${id}`, data),
  delete: (id) => api.delete(`/equipment/${id}`),
};

// Alerts API
export const alertsAPI = {
  getAll: (params = {}) => api.get('/alerts', { params }),
  getRecent: (limit = 10) => api.get('/alerts/recent', { params: { limit } }),
  getById: (id) => api.get(`/alerts/${id}`),
  acknowledge: (id, acknowledged = true) => 
    api.patch(`/alerts/${id}/acknowledge`, { acknowledged }),
  acknowledgeAll: (equipmentId = null) => {
    const params = equipmentId ? { equipment_id: equipmentId } : {};
    return api.post('/alerts/acknowledge-all', null, { params });
  },
};

// WebSocket connection
export class WebSocketClient {
  constructor() {
    this.ws = null;
    this.listeners = {
      sensor_data: [],
      alert: [],
      connection: [],
    };
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 3000;
  }

  connect(clientId = 'dashboard') {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      console.log('WebSocket already connected');
      return;
    }

    console.log('Connecting to WebSocket...');
    this.ws = new WebSocket(`${WS_URL}?client_id=${clientId}`);

    this.ws.onopen = () => {
      console.log('WebSocket connected');
      this.reconnectAttempts = 0;
      this.notifyListeners('connection', { status: 'connected' });
    };

    this.ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        this.notifyListeners(message.type, message.data);
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    this.ws.onclose = () => {
      console.log('WebSocket disconnected');
      this.notifyListeners('connection', { status: 'disconnected' });
      this.attemptReconnect();
    };
  }

  attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`Reconnecting... (Attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
      setTimeout(() => this.connect(), this.reconnectDelay);
    } else {
      console.error('Max reconnection attempts reached');
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  on(eventType, callback) {
    if (this.listeners[eventType]) {
      this.listeners[eventType].push(callback);
    }
  }

  off(eventType, callback) {
    if (this.listeners[eventType]) {
      this.listeners[eventType] = this.listeners[eventType].filter(
        (cb) => cb !== callback
      );
    }
  }

  notifyListeners(eventType, data) {
    if (this.listeners[eventType]) {
      this.listeners[eventType].forEach((callback) => callback(data));
    }
  }

  send(message) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    } else {
      console.error('WebSocket is not connected');
    }
  }
}

export const wsClient = new WebSocketClient();

export default api;
