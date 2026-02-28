# 🏭 Industrial Monitoring Dashboard

Un système complet de monitoring en temps réel pour équipements industriels avec dashboard interactif et système d'alertes automatiques.

![Dashboard Preview](https://img.shields.io/badge/Status-Production%20Ready-success)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![React](https://img.shields.io/badge/React-18.2-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)

## 📋 Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Architecture](#-architecture)
- [Stack Technique](#-stack-technique)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [API Documentation](#-api-documentation)
- [WebSocket Events](#-websocket-events)
- [Démonstration](#-démonstration)

## ✨ Fonctionnalités

### Backend
- ✅ **API REST complète** avec FastAPI
- ✅ **WebSocket** pour streaming de données en temps réel
- ✅ **Simulateur de capteurs** réaliste avec tendances et variations
- ✅ **Système d'alertes automatique** avec seuils configurables
- ✅ **Base de données PostgreSQL** avec SQLAlchemy ORM
- ✅ **Gestion d'équipements** (CRUD complet)
- ✅ **Historique des données** avec filtres temporels

### Frontend
- ✅ **Dashboard interactif** moderne et responsive
- ✅ **Graphiques temps réel** avec Recharts
- ✅ **Cartes d'équipements** avec statuts visuels
- ✅ **Notifications push** pour les alertes critiques
- ✅ **Modal de détails** avec graphiques historiques
- ✅ **WebSocket auto-reconnection**
- ✅ **Interface dark mode** optimisée

### Monitoring
- 🌡️ **Température** (10-95°C)
- 💨 **Pression** (10-160 PSI)
- 📊 **Vibration** (0.5-10 mm/s)

## 🏗️ Architecture

```
industrial-monitoring-dashboard/
├── backend/                    # API Python FastAPI
│   ├── main.py                # Application principale
│   ├── models.py              # Modèles SQLAlchemy
│   ├── schemas.py             # Schémas Pydantic
│   ├── database.py            # Configuration DB
│   ├── config.py              # Configuration app
│   ├── simulator.py           # Simulateur de capteurs
│   ├── websocket_manager.py   # Gestionnaire WebSocket
│   └── routers/               # Routes API
│       ├── equipment.py
│       └── alerts.py
├── frontend/                  # Application React
│   ├── src/
│   │   ├── App.jsx           # Composant principal
│   │   ├── components/       # Composants React
│   │   │   ├── StatCard.jsx
│   │   │   ├── EquipmentCard.jsx
│   │   │   ├── AlertsList.jsx
│   │   │   ├── RealtimeChart.jsx
│   │   │   └── EquipmentModal.jsx
│   │   └── services/
│   │       └── api.js        # Client API & WebSocket
│   └── package.json
└── docker-compose.yml         # PostgreSQL container
```

## 🛠️ Stack Technique

### Backend
- **FastAPI** - Framework web moderne et performant
- **SQLAlchemy** - ORM pour PostgreSQL
- **Pydantic** - Validation de données
- **WebSockets** - Communication temps réel
- **Uvicorn** - Serveur ASGI

### Frontend
- **React 18** - Library UI
- **Vite** - Build tool ultra-rapide
- **Recharts** - Graphiques interactifs
- **Tailwind CSS** - Styling moderne
- **Lucide React** - Icônes
- **Axios** - Client HTTP
- **date-fns** - Manipulation de dates

### Base de données
- **PostgreSQL 15** - Base de données relationnelle
- **Docker** - Containerisation

## 📦 Installation

### Prérequis
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Git

### 1. Cloner le repository

```bash
git clone 
cd industrial-monitoring-dashboard
```

### 2. Configuration de la base de données

```bash
# Démarrer PostgreSQL avec Docker
docker-compose up -d

# Vérifier que PostgreSQL est lancé
docker-compose ps
```

### 3. Installation du Backend

```bash
cd backend

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Copier le fichier .env
cp .env.example .env

# Lancer le serveur
python main.py
```

Le backend sera accessible sur `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

### 4. Installation du Frontend

```bash
# Ouvrir un nouveau terminal
cd frontend

# Installer les dépendances
npm install

# Lancer le serveur de développement
npm run dev
```

Le frontend sera accessible sur `http://localhost:3000`

## 🚀 Utilisation

### Démarrage rapide

1. **Démarrer PostgreSQL**
   ```bash
   docker-compose up -d
   ```

2. **Lancer le Backend** (Terminal 1)
   ```bash
   cd backend
   source venv/bin/activate  # ou venv\Scripts\activate sur Windows
   python main.py
   ```

3. **Lancer le Frontend** (Terminal 2)
   ```bash
   cd frontend
   npm run dev
   ```

4. **Accéder au Dashboard**
   - Ouvrir `http://localhost:3000` dans votre navigateur
   - Le simulateur démarre automatiquement
   - Les données s'affichent en temps réel

### Fonctionnalités du Dashboard

#### Vue d'ensemble
- **Stats en temps réel** : Nombre d'équipements par statut
- **Cartes d'équipements** : Vue instantanée des 3 capteurs
- **Alertes récentes** : Liste des 20 dernières alertes

#### Détails d'équipement
- Cliquer sur une carte d'équipement pour voir :
  - Graphiques historiques des 3 capteurs
  - Sélection de plage temporelle (1h, 6h, 24h, 7j)
  - Informations détaillées de l'équipement

#### Gestion des alertes
- **Reconnaissance d'alertes** : Cliquer sur le bouton X
- **Notifications push** : Activées automatiquement
- **Filtres d'alertes** : Par niveau et statut

## 📡 API Documentation

### Endpoints principaux

#### Equipment

```http
GET    /api/v1/equipment              # Liste tous les équipements
GET    /api/v1/equipment/dashboard    # Vue dashboard avec dernières mesures
GET    /api/v1/equipment/stats        # Statistiques globales
GET    /api/v1/equipment/{id}         # Détails d'un équipement
GET    /api/v1/equipment/{id}/readings # Historique des mesures
POST   /api/v1/equipment              # Créer un équipement
PATCH  /api/v1/equipment/{id}         # Modifier un équipement
DELETE /api/v1/equipment/{id}         # Supprimer un équipement
```

#### Alerts

```http
GET    /api/v1/alerts                 # Liste des alertes
GET    /api/v1/alerts/recent          # Alertes récentes
GET    /api/v1/alerts/{id}            # Détails d'une alerte
PATCH  /api/v1/alerts/{id}/acknowledge # Reconnaître une alerte
POST   /api/v1/alerts/acknowledge-all  # Reconnaître toutes les alertes
```

### Exemples de requêtes

#### Obtenir les statistiques du dashboard

```bash
curl http://localhost:8000/api/v1/equipment/stats
```

Réponse :
```json
{
  "total_equipment": 5,
  "operational_equipment": 3,
  "warning_equipment": 1,
  "critical_equipment": 1,
  "offline_equipment": 0,
  "total_alerts": 15,
  "critical_alerts": 3,
  "unacknowledged_alerts": 8
}
```

#### Créer un nouvel équipement

```bash
curl -X POST http://localhost:8000/api/v1/equipment \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Hydraulic Pump HP-100",
    "equipment_type": "pump",
    "location": "Building F - Pump Room"
  }'
```

## 🔌 WebSocket Events

### Connexion

```javascript
const ws = new WebSocket('ws://localhost:8000/ws?client_id=my-client');
```

### Messages reçus

#### Sensor Data
```json
{
  "type": "sensor_data",
  "data": {
    "equipment_id": 1,
    "equipment_name": "Compressor Unit A1",
    "sensor_type": "temperature",
    "value": 72.5,
    "timestamp": "2024-02-16T10:30:00Z",
    "status": "operational"
  }
}
```

#### Alert
```json
{
  "type": "alert",
  "data": {
    "alert_id": 42,
    "equipment_id": 1,
    "equipment_name": "Compressor Unit A1",
    "sensor_type": "temperature",
    "level": "warning",
    "message": "High temperature detected: 86.2°C (max: 85.0°C)",
    "value": 86.2,
    "timestamp": "2024-02-16T10:30:05Z"
  }
}
```

## 🎯 Configuration des seuils

Les seuils d'alerte sont configurables dans `backend/.env` :

```env
# Seuils de température (°C)
TEMPERATURE_MAX=85.0
TEMPERATURE_MIN=10.0

# Seuils de pression (PSI)
PRESSURE_MAX=150.0
PRESSURE_MIN=20.0

# Seuils de vibration (mm/s)
VIBRATION_MAX=8.0
```

## 🔍 Simulateur de capteurs

Le simulateur génère des données réalistes avec :
- **Valeurs de base** aléatoires par équipement
- **Tendances** lentes (+/- drift)
- **Variations sinusoïdales** pour patterns réalistes
- **Bruit gaussien** pour simulation réaliste
- **Génération automatique d'alertes** lors de dépassements de seuils

Intervalle de simulation : 2 secondes (configurable)

## 🎨 Démonstration

### Dashboard principal
![Dashboard](docs/dashboard-preview.png)

### Modal de détails
![Equipment Detail](docs/equipment-detail.png)

### Système d'alertes
![Alerts](docs/alerts-preview.png)

## 🧪 Tests

### Tester l'API

```bash
# Health check
curl http://localhost:8000/health

# Documentation interactive
open http://localhost:8000/docs
```

### Tester le WebSocket

```javascript
// Console du navigateur
const ws = new WebSocket('ws://localhost:8000/ws?client_id=test');
ws.onmessage = (event) => console.log(JSON.parse(event.data));
```

## 📝 Développement

### Ajouter un nouvel équipement

```python
# Dans une console Python avec l'environnement activé
from database import SessionLocal
from models import Equipment, EquipmentType, EquipmentStatus

db = SessionLocal()
new_equipment = Equipment(
    name="New Turbine T-500",
    equipment_type=EquipmentType.TURBINE,
    location="Building G",
    status=EquipmentStatus.OPERATIONAL
)
db.add(new_equipment)
db.commit()
```

### Personnaliser les graphiques

Les composants de graphiques sont dans `frontend/src/components/RealtimeChart.jsx`. Modifiez les couleurs, axes, ou style selon vos besoins.

## 🚀 Déploiement

### Production Build

**Backend:**
```bash
cd backend
pip install -r requirements.txt
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**Frontend:**
```bash
cd frontend
npm run build
# Servir le dossier dist/ avec nginx ou autre
```

### Docker (à venir)

```bash
docker-compose -f docker-compose.prod.yml up -d
```



Les contributions sont les bienvenues ! 





## 👨‍💻 Auteur

Eunock CHEDEME


