from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from database import get_db
from models import Alert, AlertLevel
import schemas
from sqlalchemy import desc

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("/", response_model=List[schemas.Alert])
def get_alerts(
    skip: int = 0,
    limit: int = 100,
    equipment_id: Optional[int] = None,
    level: Optional[AlertLevel] = None,
    acknowledged: Optional[bool] = None,
    hours: int = Query(24, ge=1, le=720),
    db: Session = Depends(get_db)
):
    """Get alerts with optional filtering"""
    time_threshold = datetime.utcnow() - timedelta(hours=hours)
    
    query = db.query(Alert).filter(Alert.timestamp >= time_threshold)
    
    if equipment_id:
        query = query.filter(Alert.equipment_id == equipment_id)
    
    if level:
        query = query.filter(Alert.level == level)
    
    if acknowledged is not None:
        query = query.filter(Alert.acknowledged == acknowledged)
    
    return query.order_by(desc(Alert.timestamp)).offset(skip).limit(limit).all()


@router.get("/recent", response_model=List[schemas.Alert])
def get_recent_alerts(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get most recent alerts"""
    return db.query(Alert).order_by(desc(Alert.timestamp)).limit(limit).all()


@router.get("/{alert_id}", response_model=schemas.Alert)
def get_alert_by_id(alert_id: int, db: Session = Depends(get_db)):
    """Get alert by ID"""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.patch("/{alert_id}/acknowledge", response_model=schemas.Alert)
def acknowledge_alert(
    alert_id: int,
    acknowledge_data: schemas.AlertAcknowledge,
    db: Session = Depends(get_db)
):
    """Acknowledge or unacknowledge an alert"""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    alert.acknowledged = acknowledge_data.acknowledged
    if acknowledge_data.acknowledged:
        alert.acknowledged_at = datetime.utcnow()
    else:
        alert.acknowledged_at = None
    
    db.commit()
    db.refresh(alert)
    return alert


@router.post("/acknowledge-all", response_model=dict)
def acknowledge_all_alerts(
    equipment_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Acknowledge all unacknowledged alerts"""
    query = db.query(Alert).filter(Alert.acknowledged == False)
    
    if equipment_id:
        query = query.filter(Alert.equipment_id == equipment_id)
    
    count = query.update(
        {"acknowledged": True, "acknowledged_at": datetime.utcnow()},
        synchronize_session=False
    )
    
    db.commit()
    
    return {"acknowledged_count": count}
