import React, { useState, useEffect, useCallback } from 'react';
import { Activity, AlertCircle, CheckCircle, XCircle, Wifi, WifiOff, Bell } from 'lucide-react';
import StatCard from './components/StatCard';
import EquipmentCard from './components/EquipmentCard';
import AlertsList from './components/AlertsList';
import EquipmentModal from './components/EquipmentModal';
import { equipmentAPI, alertsAPI, wsClient } from './services/api';

function App() {
  const [stats, setStats] = useState(null);
  const [equipment, setEquipment] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [selectedEquipment, setSelectedEquipment] = useState(null);
  const [wsConnected, setWsConnected] = useState(false);
  const [realtimeData, setRealtimeData] = useState({});
  const [loading, setLoading] = useState(true);

  // Load initial data
  useEffect(() => {
    loadDashboardData();
    loadAlerts();
  }, []);

  // Setup WebSocket
  useEffect(() => {
    wsClient.connect('dashboard-main');

    wsClient.on('connection', (data) => {
      setWsConnected(data.status === 'connected');
    });

    wsClient.on('sensor_data', handleSensorData);
    wsClient.on('alert', handleNewAlert);

    return () => {
      wsClient.disconnect();
    };
  }, []);

  const loadDashboardData = async () => {
    try {
      const [statsRes, equipmentRes] = await Promise.all([
        equipmentAPI.getStats(),
        equipmentAPI.getDashboard(),
      ]);
      setStats(statsRes.data);
      setEquipment(equipmentRes.data);
    } catch (error) {
      console.error('Error loading dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadAlerts = async () => {
    try {
      const response = await alertsAPI.getRecent(20);
      setAlerts(response.data);
    } catch (error) {
      console.error('Error loading alerts:', error);
    }
  };

  const handleSensorData = useCallback((data) => {
    const { equipment_id, sensor_type, value, timestamp, status } = data;

    // Update equipment status
    setEquipment((prev) =>
      prev.map((eq) =>
        eq.id === equipment_id
          ? {
              ...eq,
              [`latest_${sensor_type}`]: value,
              status: status,
            }
          : eq
      )
    );

    // Store realtime data for charts
    setRealtimeData((prev) => {
      const equipmentData = prev[equipment_id] || {};
      const sensorData = equipmentData[sensor_type] || [];
      
      return {
        ...prev,
        [equipment_id]: {
          ...equipmentData,
          [sensor_type]: [...sensorData, { value, timestamp }].slice(-50),
        },
      };
    });
  }, []);

  const handleNewAlert = useCallback((alertData) => {
    // Add new alert to the list
    const newAlert = {
      id: alertData.alert_id,
      equipment_id: alertData.equipment_id,
      sensor_type: alertData.sensor_type,
      level: alertData.level,
      message: alertData.message,
      value: alertData.value,
      timestamp: alertData.timestamp,
      acknowledged: false,
    };

    setAlerts((prev) => [newAlert, ...prev].slice(0, 20));

    // Update stats
    setStats((prev) => ({
      ...prev,
      total_alerts: (prev?.total_alerts || 0) + 1,
      unacknowledged_alerts: (prev?.unacknowledged_alerts || 0) + 1,
      critical_alerts:
        alertData.level === 'critical'
          ? (prev?.critical_alerts || 0) + 1
          : prev?.critical_alerts || 0,
    }));

    // Show browser notification
    if ('Notification' in window && Notification.permission === 'granted') {
      new Notification('New Alert', {
        body: `${alertData.equipment_name}: ${alertData.message}`,
        icon: '/alert-icon.png',
        tag: `alert-${alertData.alert_id}`,
      });
    }
  }, []);

  const handleAcknowledgeAlert = async (alertId) => {
    try {
      await alertsAPI.acknowledge(alertId);
      setAlerts((prev) =>
        prev.map((alert) =>
          alert.id === alertId
            ? { ...alert, acknowledged: true, acknowledged_at: new Date().toISOString() }
            : alert
        )
      );
      setStats((prev) => ({
        ...prev,
        unacknowledged_alerts: Math.max(0, (prev?.unacknowledged_alerts || 0) - 1),
      }));
    } catch (error) {
      console.error('Error acknowledging alert:', error);
    }
  };

  // Request notification permission
  useEffect(() => {
    if ('Notification' in window && Notification.permission === 'default') {
      Notification.requestPermission();
    }
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-center">
          <Activity className="w-16 h-16 text-blue-500 animate-spin mx-auto mb-4" />
          <p className="text-gray-400 text-xl">Loading Dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      {/* Header */}
      <header className="bg-gradient-to-r from-slate-900 to-slate-800 border-b border-slate-700 shadow-lg">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Activity className="w-8 h-8 text-blue-500" />
              <div>
                <h1 className="text-2xl font-bold">Industrial Monitoring Dashboard</h1>
                <p className="text-gray-400 text-sm">Real-time equipment monitoring system</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              {/* WebSocket Status */}
              <div className="flex items-center space-x-2 px-3 py-2 bg-slate-800 rounded-lg border border-slate-700">
                {wsConnected ? (
                  <>
                    <Wifi className="w-4 h-4 text-green-400" />
                    <span className="text-sm text-green-400">Connected</span>
                  </>
                ) : (
                  <>
                    <WifiOff className="w-4 h-4 text-red-400" />
                    <span className="text-sm text-red-400">Disconnected</span>
                  </>
                )}
              </div>
              
              {/* Notifications */}
              <button className="relative p-2 bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors">
                <Bell className="w-5 h-5 text-gray-400" />
                {stats && stats.unacknowledged_alerts > 0 && (
                  <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 rounded-full text-xs flex items-center justify-center font-bold">
                    {stats.unacknowledged_alerts}
                  </span>
                )}
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-8">
        {/* Stats Cards */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <StatCard
              title="Total Equipment"
              value={stats.total_equipment}
              icon={Activity}
              color="blue"
            />
            <StatCard
              title="Operational"
              value={stats.operational_equipment}
              icon={CheckCircle}
              color="green"
            />
            <StatCard
              title="Warning Status"
              value={stats.warning_equipment}
              icon={AlertCircle}
              color="yellow"
            />
            <StatCard
              title="Critical Alerts"
              value={stats.critical_alerts}
              icon={XCircle}
              color="red"
            />
          </div>
        )}

        {/* Equipment Grid */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold mb-6 flex items-center">
            <Activity className="w-6 h-6 mr-2 text-blue-500" />
            Equipment Status
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {equipment.map((eq) => (
              <EquipmentCard
                key={eq.id}
                equipment={eq}
                onClick={setSelectedEquipment}
              />
            ))}
          </div>
        </div>

        {/* Recent Alerts */}
        <div>
          <h2 className="text-2xl font-bold mb-6 flex items-center">
            <AlertCircle className="w-6 h-6 mr-2 text-yellow-500" />
            Recent Alerts
          </h2>
          <div className="bg-slate-900/50 border border-slate-700 rounded-xl p-6">
            <AlertsList alerts={alerts} onAcknowledge={handleAcknowledgeAlert} />
          </div>
        </div>
      </main>

      {/* Equipment Detail Modal */}
      {selectedEquipment && (
        <EquipmentModal
          equipment={selectedEquipment}
          onClose={() => setSelectedEquipment(null)}
          realtimeData={realtimeData}
        />
      )}
    </div>
  );
}

export default App;
