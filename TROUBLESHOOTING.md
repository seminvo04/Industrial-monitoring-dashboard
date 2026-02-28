# 🔧 Guide de Dépannage

## Problèmes courants et solutions

### 🐘 PostgreSQL

#### Problème : Docker ne démarre pas
```bash
# Vérifier que Docker Desktop est lancé
docker --version
docker ps

# Si Docker n'est pas lancé
# Windows: Ouvrir Docker Desktop
# Linux: sudo systemctl start docker
```

#### Problème : Port 5432 déjà utilisé
```bash
# Windows
netstat -ano | findstr :5432
# Trouver le PID et arrêter le processus
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5432 | xargs kill -9
# Ou changer le port dans docker-compose.yml
```

#### Problème : Cannot connect to database
```bash
# Vérifier les logs
docker-compose logs postgres

# Redémarrer le conteneur
docker-compose restart postgres

# Recréer complètement
docker-compose down
docker volume rm industrial-monitoring-dashboard_postgres_data
docker-compose up -d
```

---

### 🐍 Backend (Python)

#### Problème : Module not found
```bash
# S'assurer que l'environnement virtuel est activé
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Réinstaller les dépendances
pip install -r requirements.txt
```

#### Problème : Port 8000 déjà utilisé
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9

# Ou changer le port dans config.py
```

#### Problème : Database connection error
```bash
# Vérifier que PostgreSQL est lancé
docker ps

# Vérifier les credentials dans .env
cat backend/.env

# Test de connexion manuel
python
>>> from database import engine
>>> engine.connect()
```

#### Problème : Tables not found
```bash
# Initialiser la base de données
cd backend
python init_db.py init
python init_db.py seed
```

---

### ⚛️ Frontend (React)

#### Problème : npm install échoue
```bash
# Nettoyer le cache npm
npm cache clean --force

# Supprimer node_modules et réinstaller
rm -rf node_modules package-lock.json
npm install

# Si problème persiste, utiliser --legacy-peer-deps
npm install --legacy-peer-deps
```

#### Problème : Port 3000 déjà utilisé
```bash
# Le frontend proposera automatiquement le port 3001
# Ou forcer un port spécifique
npm run dev -- --port 3001
```

#### Problème : Cannot connect to backend
```bash
# Vérifier que le backend est lancé
curl http://localhost:8000/health

# Vérifier la configuration proxy dans vite.config.js
# Le proxy doit pointer vers http://localhost:8000
```

#### Problème : WebSocket ne se connecte pas
```bash
# 1. Vérifier que le backend WebSocket fonctionne
# Ouvrir la console du navigateur et tester :
const ws = new WebSocket('ws://localhost:8000/ws?client_id=test');
ws.onopen = () => console.log('Connected!');
ws.onerror = (e) => console.error('Error:', e);

# 2. Vérifier les CORS dans backend/config.py
# BACKEND_CORS_ORIGINS doit inclure http://localhost:3000

# 3. Vérifier le firewall
# Windows: Autoriser port 8000 dans le pare-feu
```

---

### 🔄 WebSocket

#### Problème : Déconnexions fréquentes
```javascript
// Augmenter le délai de reconnexion dans api.js
this.reconnectDelay = 5000;  // 5 secondes au lieu de 3
```

#### Problème : Pas de données en temps réel
```bash
# Vérifier que le simulateur tourne
curl http://localhost:8000/health
# Regarder "simulator_running": true

# Vérifier les logs du backend
# Devrait afficher "Client connected" quand le frontend se connecte
```

---

### 🎨 Interface

#### Problème : Graphiques ne s'affichent pas
```bash
# Vérifier la console du navigateur (F12)
# Erreurs potentielles :
# - Recharts non installé : npm install recharts
# - Date invalide : vérifier le format des timestamps
```

#### Problème : Styles cassés
```bash
# Reconstruire Tailwind
cd frontend
npm run build

# Vérifier que index.css est importé dans main.jsx
# import './index.css'
```

---

### 🧪 Tests

#### Tester l'API manuellement
```bash
# Health check
curl http://localhost:8000/health

# Stats
curl http://localhost:8000/api/v1/equipment/stats

# Equipment
curl http://localhost:8000/api/v1/equipment

# Swagger UI
# Ouvrir http://localhost:8000/docs dans un navigateur
```

#### Tester le WebSocket
```javascript
// Console du navigateur
const ws = new WebSocket('ws://localhost:8000/ws?client_id=test');

ws.onopen = () => console.log('✅ Connected');
ws.onmessage = (e) => console.log('📨', JSON.parse(e.data));
ws.onerror = (e) => console.error('❌', e);
ws.onclose = () => console.log('🔌 Disconnected');
```

---

### 📊 Performance

#### Backend lent
```bash
# Vérifier les connexions DB
# Dans config.py, ajuster :
pool_size=10
max_overflow=20

# Activer les logs de requêtes lentes
# Dans database.py, ajouter :
echo=True  # Pour voir toutes les requêtes SQL
```

#### Frontend lent
```javascript
// Dans App.jsx, réduire la fréquence de mise à jour
// Dans handleSensorData, limiter les mises à jour :
if (Date.now() - lastUpdate < 100) return;  // Max 10 FPS
```

---

### 🔐 Sécurité

#### CORS errors
```python
# Dans backend/config.py, ajouter votre origine
BACKEND_CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
]
```

---

### 📝 Logs

#### Activer les logs détaillés

**Backend:**
```python
# Dans main.py, ajouter :
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Frontend:**
```javascript
// Dans api.js, décommenter les console.log
console.log('WebSocket message:', message);
```

---

### 🆘 Réinitialisation complète

Si tout échoue, réinitialiser complètement :

```bash
# 1. Arrêter tous les services
docker-compose down
# Tuer les processus Python et Node si nécessaire

# 2. Nettoyer les données
docker volume rm industrial-monitoring-dashboard_postgres_data
rm -rf backend/venv
rm -rf frontend/node_modules

# 3. Réinstaller
docker-compose up -d

cd backend
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sur Windows
pip install -r requirements.txt
python init_db.py reset

cd ../frontend
npm install

# 4. Relancer
# Terminal 1: cd backend && python main.py
# Terminal 2: cd frontend && npm run dev
```

---

## 📞 Support

Si le problème persiste :

1. Vérifier les logs détaillés
2. Chercher l'erreur exacte sur Google/Stack Overflow
3. Ouvrir une issue sur GitHub avec :
   - Message d'erreur complet
   - Commandes exécutées
   - Système d'exploitation
   - Versions (Python, Node, Docker)

---

## ✅ Checklist de vérification

Avant de chercher des erreurs, vérifier :

- [ ] Docker Desktop est lancé
- [ ] PostgreSQL tourne (`docker ps`)
- [ ] Environnement virtuel Python activé
- [ ] Dépendances backend installées
- [ ] Dépendances frontend installées
- [ ] Fichier `.env` existe dans backend/
- [ ] Ports 5432, 8000, 3000 disponibles
- [ ] Base de données initialisée

---

Bon débogage ! 🐛
