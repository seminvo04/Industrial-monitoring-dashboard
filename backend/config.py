from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/industrial_monitoring"
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Industrial Monitoring Dashboard"
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173"]
    
    # WebSocket
    WS_MESSAGE_QUEUE_SIZE: int = 100
    
    # Simulation
    SIMULATION_INTERVAL: float = 2.0  # seconds
    
    # Alert thresholds
    TEMPERATURE_MAX: float = 85.0
    TEMPERATURE_MIN: float = 10.0
    PRESSURE_MAX: float = 150.0
    PRESSURE_MIN: float = 20.0
    VIBRATION_MAX: float = 8.0
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
