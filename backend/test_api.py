"""
Collection de tests manuels pour l'API
Pour des tests automatisés, utiliser pytest
"""

import requests
import json

BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api/v1"


def test_health_check():
    """Test du endpoint health"""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200
    print("✅ Health check passed\n")


def test_get_stats():
    """Test des statistiques du dashboard"""
    print("Testing dashboard stats...")
    response = requests.get(f"{API_URL}/equipment/stats")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200
    print("✅ Stats test passed\n")


def test_get_equipment():
    """Test de récupération des équipements"""
    print("Testing get equipment...")
    response = requests.get(f"{API_URL}/equipment")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Found {len(data)} equipment")
    if len(data) > 0:
        print(f"First equipment: {json.dumps(data[0], indent=2)}")
    assert response.status_code == 200
    print("✅ Get equipment test passed\n")


def test_get_dashboard():
    """Test du dashboard avec données en temps réel"""
    print("Testing dashboard endpoint...")
    response = requests.get(f"{API_URL}/equipment/dashboard")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Found {len(data)} equipment with latest readings")
    if len(data) > 0:
        print(f"Sample equipment: {json.dumps(data[0], indent=2)}")
    assert response.status_code == 200
    print("✅ Dashboard test passed\n")


def test_get_alerts():
    """Test de récupération des alertes"""
    print("Testing get alerts...")
    response = requests.get(f"{API_URL}/alerts/recent?limit=5")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Found {len(data)} recent alerts")
    if len(data) > 0:
        print(f"Most recent alert: {json.dumps(data[0], indent=2)}")
    assert response.status_code == 200
    print("✅ Get alerts test passed\n")


def test_create_equipment():
    """Test de création d'équipement"""
    print("Testing create equipment...")
    new_equipment = {
        "name": "Test Equipment API",
        "equipment_type": "compressor",
        "location": "Test Location",
        "status": "operational"
    }
    response = requests.post(
        f"{API_URL}/equipment",
        json=new_equipment
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        data = response.json()
        print(f"Created equipment: {json.dumps(data, indent=2)}")
        equipment_id = data['id']
        
        # Clean up - delete the test equipment
        delete_response = requests.delete(f"{API_URL}/equipment/{equipment_id}")
        print(f"Cleanup: Deleted test equipment (status: {delete_response.status_code})")
    
    assert response.status_code == 201
    print("✅ Create equipment test passed\n")


def test_get_readings():
    """Test de récupération des lectures de capteurs"""
    print("Testing get sensor readings...")
    # First, get an equipment ID
    equipment_response = requests.get(f"{API_URL}/equipment")
    if equipment_response.status_code == 200:
        equipment_list = equipment_response.json()
        if len(equipment_list) > 0:
            equipment_id = equipment_list[0]['id']
            
            # Get readings for this equipment
            response = requests.get(
                f"{API_URL}/equipment/{equipment_id}/readings",
                params={"hours": 1}
            )
            print(f"Status: {response.status_code}")
            data = response.json()
            print(f"Found {len(data)} readings for equipment {equipment_id}")
            if len(data) > 0:
                print(f"Sample reading: {json.dumps(data[0], indent=2)}")
            
            assert response.status_code == 200
            print("✅ Get readings test passed\n")
        else:
            print("⚠️  No equipment found to test readings")
    else:
        print("⚠️  Could not retrieve equipment list")


def test_acknowledge_alert():
    """Test de reconnaissance d'alerte"""
    print("Testing acknowledge alert...")
    # First, get an unacknowledged alert
    alerts_response = requests.get(
        f"{API_URL}/alerts",
        params={"acknowledged": False, "limit": 1}
    )
    
    if alerts_response.status_code == 200:
        alerts = alerts_response.json()
        if len(alerts) > 0:
            alert_id = alerts[0]['id']
            
            # Acknowledge the alert
            response = requests.patch(
                f"{API_URL}/alerts/{alert_id}/acknowledge",
                json={"acknowledged": True}
            )
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Alert {alert_id} acknowledged: {data['acknowledged']}")
            
            assert response.status_code == 200
            print("✅ Acknowledge alert test passed\n")
        else:
            print("⚠️  No unacknowledged alerts found")
    else:
        print("⚠️  Could not retrieve alerts list")


def run_all_tests():
    """Exécuter tous les tests"""
    print("="*60)
    print("Running API Tests")
    print("="*60 + "\n")
    
    try:
        test_health_check()
        test_get_stats()
        test_get_equipment()
        test_get_dashboard()
        test_get_alerts()
        test_create_equipment()
        test_get_readings()
        test_acknowledge_alert()
        
        print("="*60)
        print("✅ All tests passed!")
        print("="*60)
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
    except requests.exceptions.ConnectionError:
        print("\n❌ Could not connect to API. Make sure the backend is running on http://localhost:8000")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    run_all_tests()
