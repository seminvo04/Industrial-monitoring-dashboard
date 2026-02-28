import React from 'react';
import { AlertTriangle, AlertCircle, Info, Check, X } from 'lucide-react';
import { format } from 'date-fns';
import clsx from 'clsx';

const AlertsList = ({ alerts, onAcknowledge }) => {
  const getLevelIcon = (level) => {
    switch (level) {
      case 'critical':
        return <AlertTriangle className="w-5 h-5" />;
      case 'warning':
        return <AlertCircle className="w-5 h-5" />;
      case 'info':
        return <Info className="w-5 h-5" />;
      default:
        return <AlertCircle className="w-5 h-5" />;
    }
  };

  const getLevelStyles = (level) => {
    switch (level) {
      case 'critical':
        return 'bg-red-500/10 border-red-500/30 text-red-400';
      case 'warning':
        return 'bg-yellow-500/10 border-yellow-500/30 text-yellow-400';
      case 'info':
        return 'bg-blue-500/10 border-blue-500/30 text-blue-400';
      default:
        return 'bg-gray-500/10 border-gray-500/30 text-gray-400';
    }
  };

  if (!alerts || alerts.length === 0) {
    return (
      <div className="text-center py-12">
        <Check className="w-16 h-16 text-green-400 mx-auto mb-4" />
        <p className="text-gray-400 text-lg">No active alerts</p>
        <p className="text-gray-500 text-sm">All systems operational</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {alerts.map((alert) => (
        <div
          key={alert.id}
          className={clsx(
            'border rounded-lg p-4 transition-all',
            getLevelStyles(alert.level),
            alert.acknowledged && 'opacity-50'
          )}
        >
          <div className="flex items-start justify-between">
            <div className="flex items-start space-x-3 flex-1">
              <div className={clsx(
                'p-2 rounded-lg',
                alert.level === 'critical' && 'bg-red-500/20',
                alert.level === 'warning' && 'bg-yellow-500/20',
                alert.level === 'info' && 'bg-blue-500/20'
              )}>
                {getLevelIcon(alert.level)}
              </div>
              
              <div className="flex-1">
                <div className="flex items-center space-x-2 mb-1">
                  <h4 className="font-semibold text-white">
                    Equipment #{alert.equipment_id}
                  </h4>
                  <span className="text-xs px-2 py-0.5 bg-slate-900/50 rounded-full text-gray-400">
                    {alert.sensor_type}
                  </span>
                </div>
                
                <p className="text-sm text-gray-300 mb-2">{alert.message}</p>
                
                <div className="flex items-center space-x-4 text-xs text-gray-400">
                  <span>Value: {alert.value.toFixed(2)}</span>
                  {alert.threshold && (
                    <span>Threshold: {alert.threshold.toFixed(2)}</span>
                  )}
                  <span>{format(new Date(alert.timestamp), 'MMM dd, HH:mm:ss')}</span>
                </div>
                
                {alert.acknowledged && alert.acknowledged_at && (
                  <div className="mt-2 text-xs text-gray-500">
                    <Check className="w-3 h-3 inline mr-1" />
                    Acknowledged at {format(new Date(alert.acknowledged_at), 'MMM dd, HH:mm')}
                  </div>
                )}
              </div>
            </div>
            
            {!alert.acknowledged && onAcknowledge && (
              <button
                onClick={() => onAcknowledge(alert.id)}
                className="ml-4 p-2 bg-slate-700/50 hover:bg-slate-600/50 rounded-lg transition-colors"
                title="Acknowledge alert"
              >
                <X className="w-4 h-4 text-gray-400 hover:text-white" />
              </button>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};

export default AlertsList;
