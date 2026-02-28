from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from database import get_db
from models import Equipment, SensorReading, Alert, Sensor, SensorType, EquipmentStatus
import schemas
from sqlalchemy import func, desc

router = APIRouter(prefix="/equipment", tags=["equipment"])


@router.get("/", response_model=List[schemas.Equipment])
def get_equipment(
    skip: int = 0,
    limit: int = 100,
    status: Optional[EquipmentStatus] = None,
    db: Session = Depends(get_db)
):
    """Get all equipment with optional filtering"""
    query = db.query(Equipment)
    
    if status:
        query = query.filter(Equipment.status == status)
    
    return query.offset(skip).limit(limit).all()


@router.get("/dashboard", response_model=List[schemas.EquipmentWithLatestReadings])
def get_equipment_dashboard(db: Session = Depends(get_db)):
    """Get equipment with latest sensor readings for dashboard"""
    equipment_list = db.query(Equipment).filter(Equipment.is_active == True).all()
    
    result = []
    for equipment in equipment_list:
        # Get latest readings
        latest_temp = db.query(SensorReading).filter(
            SensorReading.equipment_id == equipment.id,
            SensorReading.sensor_type == SensorType.TEMPERATURE
        ).order_by(desc(SensorReading.timestamp)).first()
        
        latest_pressure = db.query(SensorReading).filter(
            SensorReading.equipment_id == equipment.id,
            SensorReading.sensor_type == SensorType.PRESSURE
        ).order_by(desc(SensorReading.timestamp)).first()
        
        latest_vibration = db.query(SensorReading).filter(
            SensorReading.equipment_id == equipment.id,
            SensorReading.sensor_type == SensorType.VIBRATION
        ).order_by(desc(SensorReading.timestamp)).first()
        
        # Count active alerts
        active_alerts = db.query(Alert).filter(
            Alert.equipment_id == equipment.id,
            Alert.acknowledged == False
        ).count()
        
        equipment_data = schemas.EquipmentWithLatestReadings(
            id=equipment.id,
            name=equipment.name,
            equipment_type=equipment.equipment_type,
            location=equipment.location,
            status=equipment.status,
            installed_date=equipment.installed_date,
            last_maintenance=equipment.last_maintenance,
            is_active=equipment.is_active,
            latest_temperature=latest_temp.value if latest_temp else None,
            latest_pressure=latest_pressure.value if latest_pressure else None,
            latest_vibration=latest_vibration.value if latest_vibration else None,
            active_alerts_count=active_alerts
        )
        
        result.append(equipment_data)
    
    return result


@router.get("/stats", response_model=schemas.DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics"""
    total = db.query(Equipment).filter(Equipment.is_active == True).count()
    operational = db.query(Equipment).filter(
        Equipment.status == EquipmentStatus.OPERATIONAL,
        Equipment.is_active == True
    ).count()
    warning = db.query(Equipment).filter(
        Equipment.status == EquipmentStatus.WARNING,
        Equipment.is_active == True
    ).count()
    critical = db.query(Equipment).filter(
        Equipment.status == EquipmentStatus.CRITICAL,
        Equipment.is_active == True
    ).count()
    offline = db.query(Equipment).filter(
        Equipment.status == EquipmentStatus.OFFLINE,
        Equipment.is_active == True
    ).count()
    
    total_alerts = db.query(Alert).count()
    from models import AlertLevel
    critical_alerts = db.query(Alert).filter(Alert.level == AlertLevel.CRITICAL).count()
    unacknowledged = db.query(Alert).filter(Alert.acknowledged == False).count()
    
    return schemas.DashboardStats(
        total_equipment=total,
        operational_equipment=operational,
        warning_equipment=warning,
        critical_equipment=critical,
        offline_equipment=offline,
        total_alerts=total_alerts,
        critical_alerts=critical_alerts,
        unacknowledged_alerts=unacknowledged
    )


@router.get("/{equipment_id}", response_model=schemas.Equipment)
def get_equipment_by_id(equipment_id: int, db: Session = Depends(get_db)):
    """Get equipment by ID"""
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment


@router.post("/", response_model=schemas.Equipment, status_code=201)
def create_equipment(equipment: schemas.EquipmentCreate, db: Session = Depends(get_db)):
    """Create new equipment"""
    db_equipment = Equipment(**equipment.dict())
    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)
    return db_equipment


@router.patch("/{equipment_id}", response_model=schemas.Equipment)
def update_equipment(
    equipment_id: int,
    equipment_update: schemas.EquipmentUpdate,
    db: Session = Depends(get_db)
):
    """Update equipment"""
    db_equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not db_equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    update_data = equipment_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_equipment, key, value)
    
    db.commit()
    db.refresh(db_equipment)
    return db_equipment


@router.delete("/{equipment_id}", status_code=204)
def delete_equipment(equipment_id: int, db: Session = Depends(get_db)):
    """Delete equipment (soft delete)"""
    db_equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not db_equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    db_equipment.is_active = False
    db.commit()
    return None


@router.get("/{equipment_id}/readings", response_model=List[schemas.SensorReading])
def get_equipment_readings(
    equipment_id: int,
    sensor_type: Optional[SensorType] = None,
    hours: int = Query(24, ge=1, le=168),
    db: Session = Depends(get_db)
):
    """Get sensor readings for equipment"""
    time_threshold = datetime.utcnow() - timedelta(hours=hours)
    
    query = db.query(SensorReading).filter(
        SensorReading.equipment_id == equipment_id,
        SensorReading.timestamp >= time_threshold
    )
    
    if sensor_type:
        query = query.filter(SensorReading.sensor_type == sensor_type)
    
    return query.order_by(SensorReading.timestamp).all()
