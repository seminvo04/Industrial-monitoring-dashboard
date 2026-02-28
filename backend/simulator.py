import random
import asyncio
from datetime import datetime
from typing import Dict, List
from sqlalchemy.orm import Session
from models import Equipment, SensorReading, Alert, SensorType, AlertLevel, EquipmentStatus
from config import settings
import math


class SensorSimulator:
    def __init__(self, db: Session):
        self.db = db
        self.is_running = False
        self.base_values = {}
        self.trends = {}
        
    def initialize_base_values(self):
        """Initialize base values for each equipment"""
        equipment_list = self.db.query(Equipment).filter(Equipment.is_active == True).all()
        
        for equipment in equipment_list:
            self.base_values[equipment.id] = {
                SensorType.TEMPERATURE: random.uniform(40, 70),
                SensorType.PRESSURE: random.uniform(60, 110),
                SensorType.VIBRATION: random.uniform(2, 5)
            }
            self.trends[equipment.id] = {
                SensorType.TEMPERATURE: random.uniform(-0.5, 0.5),
                SensorType.PRESSURE: random.uniform(-1, 1),
                SensorType.VIBRATION: random.uniform(-0.2, 0.2)
            }
    
    def generate_realistic_value(self, equipment_id: int, sensor_type: SensorType, 
                                 time_offset: float = 0) -> float:
        """Generate realistic sensor values with trends and noise"""
        if equipment_id not in self.base_values:
            self.initialize_base_values()
        
        base = self.base_values[equipment_id][sensor_type]
        trend = self.trends[equipment_id][sensor_type]
        
        # Add sinusoidal variation for realistic patterns
        sine_variation = math.sin(time_offset / 10) * 3
        
        # Add random noise
        noise = random.gauss(0, 1)
        
        # Combine all factors
        value = base + trend * time_offset + sine_variation + noise
        
        # Ensure values stay in reasonable ranges
        if sensor_type == SensorType.TEMPERATURE:
            value = max(15, min(95, value))
        elif sensor_type == SensorType.PRESSURE:
            value = max(10, min(160, value))
        elif sensor_type == SensorType.VIBRATION:
            value = max(0.5, min(10, value))
        
        return round(value, 2)
    
    def check_thresholds_and_create_alert(self, equipment_id: int, sensor_type: SensorType, 
                                         value: float) -> Alert:
        """Check if value exceeds thresholds and create alert if needed"""
        equipment = self.db.query(Equipment).filter(Equipment.id == equipment_id).first()
        
        alert = None
        level = None
        message = None
        threshold = None
        
        if sensor_type == SensorType.TEMPERATURE:
            if value > settings.TEMPERATURE_MAX:
                level = AlertLevel.CRITICAL if value > settings.TEMPERATURE_MAX + 5 else AlertLevel.WARNING
                message = f"High temperature detected: {value}°C (max: {settings.TEMPERATURE_MAX}°C)"
                threshold = settings.TEMPERATURE_MAX
            elif value < settings.TEMPERATURE_MIN:
                level = AlertLevel.WARNING
                message = f"Low temperature detected: {value}°C (min: {settings.TEMPERATURE_MIN}°C)"
                threshold = settings.TEMPERATURE_MIN
                
        elif sensor_type == SensorType.PRESSURE:
            if value > settings.PRESSURE_MAX:
                level = AlertLevel.CRITICAL if value > settings.PRESSURE_MAX + 10 else AlertLevel.WARNING
                message = f"High pressure detected: {value} PSI (max: {settings.PRESSURE_MAX} PSI)"
                threshold = settings.PRESSURE_MAX
            elif value < settings.PRESSURE_MIN:
                level = AlertLevel.WARNING
                message = f"Low pressure detected: {value} PSI (min: {settings.PRESSURE_MIN} PSI)"
                threshold = settings.PRESSURE_MIN
                
        elif sensor_type == SensorType.VIBRATION:
            if value > settings.VIBRATION_MAX:
                level = AlertLevel.CRITICAL if value > settings.VIBRATION_MAX + 1 else AlertLevel.WARNING
                message = f"High vibration detected: {value} mm/s (max: {settings.VIBRATION_MAX} mm/s)"
                threshold = settings.VIBRATION_MAX
        
        if level and message:
            alert = Alert(
                equipment_id=equipment_id,
                sensor_type=sensor_type,
                level=level,
                message=message,
                value=value,
                threshold=threshold
            )
            self.db.add(alert)
            
            # Update equipment status
            if level == AlertLevel.CRITICAL and equipment.status != EquipmentStatus.CRITICAL:
                equipment.status = EquipmentStatus.CRITICAL
            elif level == AlertLevel.WARNING and equipment.status == EquipmentStatus.OPERATIONAL:
                equipment.status = EquipmentStatus.WARNING
            
            self.db.commit()
            self.db.refresh(alert)
        
        return alert
    
    async def generate_reading(self, equipment_id: int, time_offset: float = 0) -> Dict:
        """Generate a complete set of sensor readings for an equipment"""
        readings = {}
        alerts = []
        
        for sensor_type in [SensorType.TEMPERATURE, SensorType.PRESSURE, SensorType.VIBRATION]:
            value = self.generate_realistic_value(equipment_id, sensor_type, time_offset)
            
            # Create sensor reading
            reading = SensorReading(
                equipment_id=equipment_id,
                sensor_type=sensor_type,
                value=value,
                timestamp=datetime.utcnow()
            )
            self.db.add(reading)
            readings[sensor_type.value] = value
            
            # Check for alerts
            alert = self.check_thresholds_and_create_alert(equipment_id, sensor_type, value)
            if alert:
                alerts.append(alert)
        
        self.db.commit()
        
        return {
            "equipment_id": equipment_id,
            "readings": readings,
            "alerts": alerts,
            "timestamp": datetime.utcnow()
        }
    
    async def simulate_continuous(self, callback=None):
        """Continuously generate sensor data"""
        self.is_running = True
        self.initialize_base_values()
        time_offset = 0
        
        while self.is_running:
            equipment_list = self.db.query(Equipment).filter(Equipment.is_active == True).all()
            
            for equipment in equipment_list:
                data = await self.generate_reading(equipment.id, time_offset)
                
                if callback:
                    await callback(data)
            
            time_offset += 1
            await asyncio.sleep(settings.SIMULATION_INTERVAL)
    
    def stop(self):
        """Stop the simulation"""
        self.is_running = False
