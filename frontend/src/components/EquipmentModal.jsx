import React, { useState, useEffect } from 'react';
import { X, Download, RefreshCw } from 'lucide-react';
import RealtimeChart from './RealtimeChart';
import { equipmentAPI } from '../services/api';

const EquipmentModal = ({ equipment, onClose, realtimeData }) => {
  const [historicalData, setHistoricalData] = useState({
    temperature: [],
    pressure: [],
    vibration: [],
  });
  const [loading, setLoading] = useState(false);
  const [timeRange, setTimeRange] = useState(24);

  useEffect(() => {
    if (equipment) {
      loadHistoricalData();
    }
  }, [equipment, timeRange]);

  const loadHistoricalData = async () => {
    if (!equipment) return;
    
    setLoading(true);
    try {
      const [tempData, pressureData, vibrationData] = await Promise.all([
        equipmentAPI.getReadings(equipment.id, 'temperature', timeRange),
        equipmentAPI.getReadings(equipment.id, 'pressure', timeRange),
        equipmentAPI.getReadings(equipment.id, 'vibration', timeRange),
      ]);

      setHistoricalData({
        temperature: tempData.data,
        pressure: pressureData.data,
        vibration: vibrationData.data,
      });
    } catch (error) {
      console.error('Error loading historical data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!equipment) return null;

  // Combine historical and realtime data
  const getChartData = (sensorType) => {
    const historical = historicalData[sensorType] || [];
    const realtime = realtimeData[equipment.id]?.[sensorType] || [];
    return [...historical, ...realtime];
  };

  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-6xl w-full max-h-[90vh] overflow-hidden shadow-2xl">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600/20 to-purple-600/20 border-b border-slate-700 p-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold text-white mb-1">{equipment.name}</h2>
              <p className="text-gray-400">{equipment.location}</p>
            </div>
            <div className="flex items-center space-x-3">
              <select
                value={timeRange}
                onChange={(e) => setTimeRange(Number(e.target.value))}
                className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value={1}>Last 1 hour</option>
                <option value={6}>Last 6 hours</option>
                <option value={24}>Last 24 hours</option>
                <option value={168}>Last 7 days</option>
              </select>
              
              <button
                onClick={loadHistoricalData}
                disabled={loading}
                className="p-2 bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors disabled:opacity-50"
                title="Refresh data"
              >
                <RefreshCw className={`w-5 h-5 text-gray-400 ${loading ? 'animate-spin' : ''}`} />
              </button>
              
              <button
                onClick={onClose}
                className="p-2 bg-slate-800 hover:bg-red-600/20 rounded-lg transition-colors"
              >
                <X className="w-5 h-5 text-gray-400 hover:text-red-400" />
              </button>
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto max-h-[calc(90vh-120px)] scrollbar-hide">
          {loading && !historicalData.temperature.length ? (
            <div className="flex items-center justify-center py-20">
              <RefreshCw className="w-8 h-8 text-blue-400 animate-spin" />
              <span className="ml-3 text-gray-400">Loading data...</span>
            </div>
          ) : (
            <div className="space-y-6">
              {/* Temperature Chart */}
              <RealtimeChart
                data={getChartData('temperature')}
                title="Temperature"
                dataKey="value"
                color="#f97316"
                unit="°C"
              />

              {/* Pressure Chart */}
              <RealtimeChart
                data={getChartData('pressure')}
                title="Pressure"
                dataKey="value"
                color="#3b82f6"
                unit="PSI"
              />

              {/* Vibration Chart */}
              <RealtimeChart
                data={getChartData('vibration')}
                title="Vibration"
                dataKey="value"
                color="#a855f7"
                unit="mm/s"
              />

              {/* Equipment Info */}
              <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-5">
                <h3 className="text-lg font-semibold text-white mb-4">Equipment Information</h3>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <p className="text-gray-400 mb-1">Type</p>
                    <p className="text-white font-medium capitalize">{equipment.equipment_type}</p>
                  </div>
                  <div>
                    <p className="text-gray-400 mb-1">Status</p>
                    <p className="text-white font-medium capitalize">{equipment.status}</p>
                  </div>
                  <div>
                    <p className="text-gray-400 mb-1">Installed Date</p>
                    <p className="text-white font-medium">
                      {new Date(equipment.installed_date).toLocaleDateString()}
                    </p>
                  </div>
                  <div>
                    <p className="text-gray-400 mb-1">Last Maintenance</p>
                    <p className="text-white font-medium">
                      {equipment.last_maintenance
                        ? new Date(equipment.last_maintenance).toLocaleDateString()
                        : 'Never'}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default EquipmentModal;
