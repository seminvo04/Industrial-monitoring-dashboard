from fastapi import WebSocket, WebSocketDisconnect
from typing import List, Dict
import json
from datetime import datetime
import asyncio


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.connection_info: Dict[WebSocket, dict] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str = None):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.connection_info[websocket] = {
            "client_id": client_id,
            "connected_at": datetime.utcnow()
        }
        print(f"Client {client_id} connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            client_info = self.connection_info.pop(websocket, {})
            print(f"Client {client_info.get('client_id')} disconnected. Total connections: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        try:
            await websocket.send_json(message)
        except Exception as e:
            print(f"Error sending personal message: {e}")
            self.disconnect(websocket)
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except WebSocketDisconnect:
                disconnected.append(connection)
            except Exception as e:
                print(f"Error broadcasting to client: {e}")
                disconnected.append(connection)
        
        # Clean up disconnected clients
        for connection in disconnected:
            self.disconnect(connection)
    
    async def broadcast_sensor_data(self, equipment_id: int, equipment_name: str, 
                                   readings: dict, timestamp: datetime, status: str):
        """Broadcast sensor readings to all clients"""
        for sensor_type, value in readings.items():
            message = {
                "type": "sensor_data",
                "data": {
                    "equipment_id": equipment_id,
                    "equipment_name": equipment_name,
                    "sensor_type": sensor_type,
                    "value": value,
                    "timestamp": timestamp.isoformat(),
                    "status": status
                }
            }
            await self.broadcast(message)
    
    async def broadcast_alert(self, alert):
        """Broadcast alert to all clients"""
        from models import Equipment
        
        message = {
            "type": "alert",
            "data": {
                "alert_id": alert.id,
                "equipment_id": alert.equipment_id,
                "equipment_name": alert.equipment.name if alert.equipment else "Unknown",
                "sensor_type": alert.sensor_type.value,
                "level": alert.level.value,
                "message": alert.message,
                "value": alert.value,
                "timestamp": alert.timestamp.isoformat()
            }
        }
        await self.broadcast(message)
    
    def get_connection_count(self) -> int:
        return len(self.active_connections)


# Global connection manager instance
manager = ConnectionManager()
