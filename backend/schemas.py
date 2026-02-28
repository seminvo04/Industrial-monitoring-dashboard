from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from models import EquipmentType, EquipmentStatus, SensorType, AlertLevel


# Equipment schemas
class EquipmentBase(BaseModel):
    name: str
    equipment_type: EquipmentType
    location: Optional[str] = None
    status: EquipmentStatus = EquipmentStatus.OPERATIONAL


class EquipmentCreate(EquipmentBase):
    pass


class EquipmentUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    status: Optional[EquipmentStatus] = None
    last_maintenance: Optional[datetime] = None


class Equipment(EquipmentBase):
    id: int
    installed_date: datetime
    last_maintenance: Optional[datetime]
    is_active: bool

    class Config:
        from_attributes = True


# Sensor schemas
class SensorBase(BaseModel):
    sensor_type: SensorType
    unit: str
    min_threshold: Optional[float] = None
    max_threshold: Optional[float] = None


class SensorCreate(SensorBase):
    equipment_id: int


class Sensor(SensorBase):
    id: int
    equipment_id: int
    is_active: bool

    class Config:
        from_attributes = True


# Sensor reading schemas
class SensorReadingBase(BaseModel):
    equipment_id: int
    sensor_type: SensorType
    value: float


class SensorReadingCreate(SensorReadingBase):
    pass


class SensorReading(SensorReadingBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True


# Alert schemas
class AlertBase(BaseModel):
    equipment_id: int
    sensor_type: SensorType
    level: AlertLevel
    message: str
    value: float
    threshold: Optional[float] = None


class AlertCreate(AlertBase):
    pass


class Alert(AlertBase):
    id: int
    timestamp: datetime
    acknowledged: bool
    acknowledged_at: Optional[datetime]

    class Config:
        from_attributes = True


class AlertAcknowledge(BaseModel):
    acknowledged: bool


# Dashboard schemas
class EquipmentWithLatestReadings(Equipment):
    latest_temperature: Optional[float] = None
    latest_pressure: Optional[float] = None
    latest_vibration: Optional[float] = None
    active_alerts_count: int = 0


class DashboardStats(BaseModel):
    total_equipment: int
    operational_equipment: int
    warning_equipment: int
    critical_equipment: int
    offline_equipment: int
    total_alerts: int
    critical_alerts: int
    unacknowledged_alerts: int


# WebSocket schemas
class SensorDataMessage(BaseModel):
    equipment_id: int
    equipment_name: str
    sensor_type: str
    value: float
    timestamp: datetime
    status: str


class AlertMessage(BaseModel):
    alert_id: int
    equipment_id: int
    equipment_name: str
    sensor_type: str
    level: str
    message: str
    value: float
    timestamp: datetime
