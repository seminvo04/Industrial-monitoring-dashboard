"""
Script d'initialisation de la base de données
Crée les tables et insère des données de test
"""
from database import engine
from models import Base, Equipment, EquipmentType, EquipmentStatus
from database import SessionLocal
from datetime import datetime, timedelta
import random


def init_database():
    """Créer toutes les tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")


def seed_equipment():
    """Insérer des équipements de test"""
    db = SessionLocal()
    
    # Vérifier si des équipements existent déjà
    if db.query(Equipment).count() > 0:
        print("⚠️  Equipment already exists in database")
        db.close()
        return
    
    print("Seeding equipment data...")
    
    equipment_data = [
        {
            "name": "Compressor Unit A1",
            "equipment_type": EquipmentType.COMPRESSOR,
            "location": "Building A - Floor 1",
            "status": EquipmentStatus.OPERATIONAL,
            "installed_date": datetime.utcnow() - timedelta(days=365),
            "last_maintenance": datetime.utcnow() - timedelta(days=30)
        },
        {
            "name": "Water Pump B2",
            "equipment_type": EquipmentType.PUMP,
            "location": "Building B - Floor 2",
            "status": EquipmentStatus.OPERATIONAL,
            "installed_date": datetime.utcnow() - timedelta(days=730),
            "last_maintenance": datetime.utcnow() - timedelta(days=45)
        },
        {
            "name": "Electric Motor C3",
            "equipment_type": EquipmentType.MOTOR,
            "location": "Building C - Floor 3",
            "status": EquipmentStatus.OPERATIONAL,
            "installed_date": datetime.utcnow() - timedelta(days=550),
            "last_maintenance": datetime.utcnow() - timedelta(days=20)
        },
        {
            "name": "Turbine Generator D1",
            "equipment_type": EquipmentType.TURBINE,
            "location": "Building D - Main Hall",
            "status": EquipmentStatus.OPERATIONAL,
            "installed_date": datetime.utcnow() - timedelta(days=900),
            "last_maintenance": datetime.utcnow() - timedelta(days=15)
        },
        {
            "name": "Power Generator E2",
            "equipment_type": EquipmentType.GENERATOR,
            "location": "Building E - Generator Room",
            "status": EquipmentStatus.OPERATIONAL,
            "installed_date": datetime.utcnow() - timedelta(days=450),
            "last_maintenance": datetime.utcnow() - timedelta(days=60)
        },
        {
            "name": "Hydraulic Pump F3",
            "equipment_type": EquipmentType.PUMP,
            "location": "Building F - Pump Station",
            "status": EquipmentStatus.OPERATIONAL,
            "installed_date": datetime.utcnow() - timedelta(days=280),
            "last_maintenance": datetime.utcnow() - timedelta(days=10)
        },
    ]
    
    for eq_data in equipment_data:
        equipment = Equipment(**eq_data)
        db.add(equipment)
    
    db.commit()
    count = db.query(Equipment).count()
    print(f"✅ Added {count} equipment to database!")
    db.close()


def reset_database():
    """Réinitialiser complètement la base de données"""
    print("⚠️  Resetting database (this will delete all data)...")
    response = input("Are you sure? (yes/no): ")
    
    if response.lower() == 'yes':
        Base.metadata.drop_all(bind=engine)
        print("✅ All tables dropped")
        init_database()
        seed_equipment()
        print("✅ Database reset complete!")
    else:
        print("❌ Reset cancelled")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "init":
            init_database()
        elif command == "seed":
            seed_equipment()
        elif command == "reset":
            reset_database()
        else:
            print("Unknown command. Use: init, seed, or reset")
    else:
        print("Usage: python init_db.py [init|seed|reset]")
        print("  init  - Create database tables")
        print("  seed  - Add sample equipment")
        print("  reset - Reset database (WARNING: deletes all data)")
