# 🚀 Guide de Démarrage Rapide

## Installation en 5 minutes

### 1️⃣ Prérequis
- Python 3.11+ installé
- Node.js 18+ installé
- Docker Desktop installé et lancé

### 2️⃣ Lancer PostgreSQL
```bash
docker-compose up -d
```
✅ Base de données prête !

### 3️⃣ Lancer le Backend

**Terminal 1:**
```bash
cd backend
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
python main.py
```

✅ Backend lancé sur http://localhost:8000

### 4️⃣ Lancer le Frontend

**Terminal 2:**
```bash
cd frontend
npm install
npm run dev
```

✅ Frontend lancé sur http://localhost:3000

### 5️⃣ Accéder au Dashboard

Ouvrir dans votre navigateur : **http://localhost:3000**

🎉 **C'est tout !** Le simulateur génère automatiquement des données.

---

## 📊 Ce que vous allez voir

1. **5 équipements industriels** pré-configurés
2. **Données en temps réel** toutes les 2 secondes
3. **Graphiques animés** pour température, pression, vibration
4. **Alertes automatiques** quand les seuils sont dépassés

---

## 🔍 Pour tester

### Voir l'API documentation
http://localhost:8000/docs

### Vérifier la santé du système
http://localhost:8000/health

### Tester le WebSocket (Console navigateur)
```javascript
const ws = new WebSocket('ws://localhost:8000/ws?client_id=test');
ws.onmessage = (e) => console.log(JSON.parse(e.data));
```

---

## 🛑 Arrêter les services

```bash
# Arrêter le frontend: Ctrl+C dans le terminal

# Arrêter le backend: Ctrl+C dans le terminal

# Arrêter PostgreSQL:
docker-compose down
```

---

## ❓ Problèmes courants

### Port 8000 déjà utilisé
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Port 3000 déjà utilisé
```bash
# Le frontend vous proposera automatiquement le port 3001
```

### PostgreSQL n'est pas accessible
```bash
# Vérifier que Docker est lancé
docker ps

# Relancer PostgreSQL
docker-compose restart
```

---

## 🎯 Prochaines étapes

1. ✅ Cliquer sur une carte d'équipement pour voir les détails
2. ✅ Reconnaître des alertes
3. ✅ Explorer l'API avec Swagger UI
4. ✅ Modifier les seuils dans `backend/.env`

---

Bon monitoring ! 🏭
