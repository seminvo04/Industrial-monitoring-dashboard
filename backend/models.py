from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()


class EquipmentType(enum.Enum):
    COMPRESSOR = "compressor"
    PUMP = "pump"
    MOTOR = "motor"
    TURBINE = "turbine"
    GENERATOR = "generator"


class EquipmentStatus(enum.Enum):
    OPERATIONAL = "operational"
    WARNING = "warning"
    CRITICAL = "critical"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"


class SensorType(enum.Enum):
    TEMPERATURE = "temperature"
    PRESSURE = "pressure"
    VIBRATION = "vibration"


class AlertLevel(enum.Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class Equipment(Base):
    __tablename__ = "equipment"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    equipment_type = Column(SQLEnum(EquipmentType), nullable=False)
    location = Column(String(200))
    status = Column(SQLEnum(EquipmentStatus), default=EquipmentStatus.OPERATIONAL)
    installed_date = Column(DateTime, default=datetime.utcnow)
    last_maintenance = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    sensors = relationship("Sensor", back_populates="equipment", cascade="all, delete-orphan")
    readings = relationship("SensorReading", back_populates="equipment", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="equipment", cascade="all, delete-orphan")


class Sensor(Base):
    __tablename__ = "sensors"
    
    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    sensor_type = Column(SQLEnum(SensorType), nullable=False)
    unit = Column(String(20))
    min_threshold = Column(Float, nullable=True)
    max_threshold = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    equipment = relationship("Equipment", back_populates="sensors")


class SensorReading(Base):
    __tablename__ = "sensor_readings"
    
    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    sensor_type = Column(SQLEnum(SensorType), nullable=False)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    equipment = relationship("Equipment", back_populates="readings")


class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    sensor_type = Column(SQLEnum(SensorType), nullable=False)
    level = Column(SQLEnum(AlertLevel), nullable=False)
    message = Column(String(500), nullable=False)
    value = Column(Float, nullable=False)
    threshold = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    acknowledged = Column(Boolean, default=False)
    acknowledged_at = Column(DateTime, nullable=True)
    
    # Relationships
    equipment = relationship("Equipment", back_populates="alerts")
