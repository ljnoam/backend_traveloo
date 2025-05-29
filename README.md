# ✈️ Traveloo Backend – FastAPI

Backend du projet Traveloo – une plateforme de planification de voyages personnalisés avec recherche de vols, génération d'itinéraires sur mesure via IA et gestion des favoris/hôtels.

---

## 🧠 Stack technique

- **Langage** : Python 3.11
- **Framework** : FastAPI
- **API IA** : Gemini (Google Generative AI)
- **Vols** : TravelPayouts API
- **Base de données** : Supabase (PostgreSQL)
- **Docker** : Build prod-ready avec Gunicorn + UvicornWorker

---

## 🚀 Lancement rapide (prod)

### 1. Cloner le repo

```bash
git clone https://github.com/ton-user/traveloo-backend.git
cd traveloo-backend
```

### 2. Créer un fichier `.env`

Créer un fichier `.env` à partir de ce template :

```bash
cp .env.template .env
```

Remplis les variables sensibles : clés API, URL Supabase, etc.

### 3. Lancer avec Docker

```bash
docker build -t traveloo-backend .
docker run -d -p 8000:8000 --env-file .env traveloo-backend
```

✅ L'API sera dispo sur `http://localhost:8000`

---

## 🔧 Structure des dossiers

```
backend/
├── main.py               # Entrée FastAPI
├── models.py             # Schémas Pydantic
├── routes/               # Routes API REST
│   ├── auth.py
│   ├── admin.py
│   └── favorites.py
├── services/             # Logique métier
│   ├── auth.py
│   ├── flights.py
│   └── itinerary.py
├── utils/                # Utils de parsing / signature
├── Dockerfile            # Build prod
├── requirements.txt      # Dépendances
└── .env.template         # Variables d'environnement (exemple)
```

---

## 🔐 Variables d’environnement

Extrait de `.env` :

```env
FLIGHT_API_MARKER=...
FLIGHT_API_TOKEN=...
HOST=traveloo.fr
GEMINI_API_KEY=...
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=...
ENV=prod
```

---

## 📦 Endpoints principaux

| Méthode | URL                   | Description |
|--------|------------------------|-------------|
| POST   | `/api/search`          | Recherche de vols (TravelPayouts) |
| POST   | `/generate-itinerary`  | Génère un itinéraire via Gemini |
| POST   | `/auth/login`          | Connexion utilisateur |
| POST   | `/auth/register`       | Création de compte |
| GET    | `/auth/me`             | Récupère le profil |
| PUT    | `/auth/update-profile` | Modifie le profil |
| GET    | `/favorites/`          | Favoris utilisateur |
| POST   | `/favorites/`          | Ajouter un favori |
| DELETE | `/favorites/{id}`      | Supprimer un favori |
| GET    | `/admin/data`          | Vue admin : feedbacks + favoris |

---

## 🔐 Sécurité & bonnes pratiques

- Pas de docs publiques en prod (`/docs`, `/redoc`, etc.)
- Clés API chargées via `.env`, jamais exposées
- Middleware CORS restreint à `https://traveloo.fr`
- Logger intégré + handler global d’erreurs
- Docker optimisé pour prod (`gunicorn`, `uvicorn`, image slim)

---

## 🧪 À implémenter (roadmap)

- Tests unitaires et intégration
- Rate-limiting sur les endpoints IA
- Monitoring / alerting (Sentry, Datadog…)