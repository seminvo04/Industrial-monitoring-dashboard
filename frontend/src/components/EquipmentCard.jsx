import React from 'react';
import { Thermometer, Gauge, Activity, MapPin, AlertTriangle } from 'lucide-react';
import clsx from 'clsx';

const EquipmentCard = ({ equipment, onClick }) => {
  const statusStyles = {
    operational: 'status-operational',
    warning: 'status-warning',
    critical: 'status-critical',
    offline: 'status-offline',
    maintenance: 'status-maintenance',
  };

  const typeIcons = {
    compressor: '🔧',
    pump: '💧',
    motor: '⚡',
    turbine: '🌀',
    generator: '⚙️',
  };

  const formatValue = (value, decimals = 1) => {
    return value !== null && value !== undefined ? value.toFixed(decimals) : '--';
  };

  return (
    <div
      onClick={() => onClick(equipment)}
      className="bg-slate-800/50 border border-slate-700 rounded-xl p-5 hover:border-blue-500/50 hover:shadow-lg hover:shadow-blue-500/10 transition-all cursor-pointer group"
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className="text-3xl">{typeIcons[equipment.equipment_type] || '🏭'}</div>
          <div>
            <h3 className="text-lg font-semibold text-white group-hover:text-blue-400 transition-colors">
              {equipment.name}
            </h3>
            <div className="flex items-center space-x-1 text-xs text-gray-400 mt-1">
              <MapPin className="w-3 h-3" />
              <span>{equipment.location || 'Unknown location'}</span>
            </div>
          </div>
        </div>
        
        {/* Status Badge */}
        <span className={clsx(
          'px-3 py-1 rounded-full text-xs font-medium border',
          statusStyles[equipment.status]
        )}>
          {equipment.status}
        </span>
      </div>

      {/* Sensor Readings */}
      <div className="grid grid-cols-3 gap-3 mb-4">
        {/* Temperature */}
        <div className="bg-slate-900/50 rounded-lg p-3 border border-slate-700/50">
          <div className="flex items-center space-x-2 mb-1">
            <Thermometer className="w-4 h-4 text-orange-400" />
            <span className="text-xs text-gray-400">Temp</span>
          </div>
          <p className="text-lg font-bold text-white">
            {formatValue(equipment.latest_temperature)}°C
          </p>
        </div>

        {/* Pressure */}
        <div className="bg-slate-900/50 rounded-lg p-3 border border-slate-700/50">
          <div className="flex items-center space-x-2 mb-1">
            <Gauge className="w-4 h-4 text-blue-400" />
            <span className="text-xs text-gray-400">Press</span>
          </div>
          <p className="text-lg font-bold text-white">
            {formatValue(equipment.latest_pressure)} PSI
          </p>
        </div>

        {/* Vibration */}
        <div className="bg-slate-900/50 rounded-lg p-3 border border-slate-700/50">
          <div className="flex items-center space-x-2 mb-1">
            <Activity className="w-4 h-4 text-purple-400" />
            <span className="text-xs text-gray-400">Vib</span>
          </div>
          <p className="text-lg font-bold text-white">
            {formatValue(equipment.latest_vibration)} mm/s
          </p>
        </div>
      </div>

      {/* Active Alerts */}
      {equipment.active_alerts_count > 0 && (
        <div className="flex items-center space-x-2 p-2 bg-red-500/10 border border-red-500/30 rounded-lg">
          <AlertTriangle className="w-4 h-4 text-red-400 animate-pulse" />
          <span className="text-sm text-red-400 font-medium">
            {equipment.active_alerts_count} active alert{equipment.active_alerts_count > 1 ? 's' : ''}
          </span>
        </div>
      )}
    </div>
  );
};

export default EquipmentCard;
