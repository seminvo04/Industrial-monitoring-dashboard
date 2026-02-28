from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import asyncio
from contextlib import asynccontextmanager

from config import settings
from database import get_db, engine
from models import Base, Equipment, EquipmentType, EquipmentStatus
from routers import equipment, alerts
from simulator import SensorSimulator
from websocket_manager import manager


# Global simulator instance
simulator_task = None
simulator_instance = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for the application"""
    global simulator_task, simulator_instance
    
    # Startup
    print("Starting Industrial Monitoring Dashboard...")
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created")
    
    # Initialize database with sample equipment if empty
    db = next(get_db())
    if db.query(Equipment).count() == 0:
        print("Initializing sample equipment...")
        sample_equipment = [
            Equipment(
                name="Compressor Unit A1",
                equipment_type=EquipmentType.COMPRESSOR,
                location="Building A - Floor 1",
                status=EquipmentStatus.OPERATIONAL
            ),
            Equipment(
                name="Water Pump B2",
                equipment_type=EquipmentType.PUMP,
                location="Building B - Floor 2",
                status=EquipmentStatus.OPERATIONAL
            ),
            Equipment(
                name="Electric Motor C3",
                equipment_type=EquipmentType.MOTOR,
                location="Building C - Floor 3",
                status=EquipmentStatus.OPERATIONAL
            ),
            Equipment(
                name="Turbine Generator D1",
                equipment_type=EquipmentType.TURBINE,
                location="Building D - Main Hall",
                status=EquipmentStatus.OPERATIONAL
            ),
            Equipment(
                name="Power Generator E2",
                equipment_type=EquipmentType.GENERATOR,
                location="Building E - Generator Room",
                status=EquipmentStatus.OPERATIONAL
            )
        ]
        
        for equipment in sample_equipment:
            db.add(equipment)
        db.commit()
        print(f"Added {len(sample_equipment)} sample equipment")
    
    # Start simulator
    print("Starting sensor data simulator...")
    simulator_instance = SensorSimulator(db)
    
    async def data_callback(data):
        """Callback for simulator to send data via WebSocket"""
        equipment = db.query(Equipment).filter(Equipment.id == data["equipment_id"]).first()
        if equipment:
            await manager.broadcast_sensor_data(
                equipment_id=equipment.id,
                equipment_name=equipment.name,
                readings=data["readings"],
                timestamp=data["timestamp"],
                status=equipment.status.value
            )
            
            # Broadcast alerts
            for alert in data.get("alerts", []):
                await manager.broadcast_alert(alert)
    
    simulator_task = asyncio.create_task(simulator_instance.simulate_continuous(data_callback))
    print("Simulator started")
    
    yield
    
    # Shutdown
    print("Shutting down...")
    if simulator_instance:
        simulator_instance.stop()
    if simulator_task:
        simulator_task.cancel()
        try:
            await simulator_task
        except asyncio.CancelledError:
            pass
    print("Shutdown complete")


# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(equipment.router, prefix=settings.API_V1_PREFIX)
app.include_router(alerts.router, prefix=settings.API_V1_PREFIX)


@app.get("/")
async def root():
    return {
        "message": "Industrial Monitoring Dashboard API",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "equipment": f"{settings.API_V1_PREFIX}/equipment",
            "alerts": f"{settings.API_V1_PREFIX}/alerts",
            "websocket": "/ws"
        }
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "simulator_running": simulator_instance.is_running if simulator_instance else False,
        "active_connections": manager.get_connection_count()
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time data streaming"""
    client_id = websocket.query_params.get("client_id", "unknown")
    
    await manager.connect(websocket, client_id)
    
    # Send welcome message
    await manager.send_personal_message({
        "type": "connection",
        "message": "Connected to Industrial Monitoring Dashboard",
        "client_id": client_id
    }, websocket)
    
    try:
        while True:
            # Keep connection alive and handle incoming messages
            data = await websocket.receive_text()
            # Echo back or handle commands if needed
            await manager.send_personal_message({
                "type": "echo",
                "message": f"Received: {data}"
            }, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
