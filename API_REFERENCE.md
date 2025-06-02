# 📚 API Reference – Traveloo Backend (FastAPI)

Ce document liste tous les endpoints disponibles, les données attendues en entrée et les réponses renvoyées. À transmettre aux développeurs frontend ✅

---

## 🔐 Authentification

### `POST /auth/register`
**Créer un compte utilisateur**

#### Body JSON :
```json
{
  "email": "user@example.com",
  "password": "monSuperMotDePasse"
}
```

#### Réponse :
```json
{
  "user": {
    "id": "...",
    "email": "..."
  },
  "session": {
    "access_token": "...",
    ...
  }
}
```

---

### `POST /auth/login`
**Connexion utilisateur**

#### Body JSON :
```json
{
  "email": "user@example.com",
  "password": "monSuperMotDePasse"
}
```

#### Réponse :
Identique à `/auth/register`

---

### `GET /auth/me`
**Récupérer les infos du profil connecté**  
🔐 Requiert un token

#### Headers :
```
Authorization: Bearer <token>
```

#### Réponse :
```json
{
  "id": "...",
  "email": "...",
  "full_name": "Nom",
  "avatar_url": "https://...",
  "role": "user"
}
```

---

### `PUT /auth/update-profile`
**Modifier son profil utilisateur**  
🔐 Requiert un token

#### Body JSON (partiel possible) :
```json
{
  "full_name": "Jean Test",
  "avatar_url": "https://..."
}
```

#### Réponse :
```json
{
  "full_name": "Jean Test",
  "avatar_url": "https://..."
}
```

---

## ✈️ Recherche de vols

### `POST /api/search`
**Rechercher des vols avec TravelPayouts**

#### Body JSON :
```json
{
  "origin": "PAR",
  "destination": "LIS",
  "departure_date": "2025-08-01",
  "return_date": "2025-08-15",
  "class_": "Y",
  "adults": 1,
  "children": 0,
  "infants": 0
}
```

#### Réponse :
```json
{
  "itineraries": [...],
  "airlines": {...},
  ...
}
```

---

## 🤖 Génération d’itinéraire IA

### `POST /generate-itinerary`
**Créer un planning de voyage personnalisé**

#### Body JSON :
```json
{
  "city": "Lisbonne",
  "start_date": "2025-08-10",
  "end_date": "2025-08-15",
  "profile": "aventurier solo",
  "preferences": ["musées", "nourriture locale"]
}
```

#### Réponse :
```json
{
  "itinerary": [
    {
      "day": 1,
      "activities": ["Visite de l'Alfama", "Dégustation de pastel de nata"]
    },
    ...
  ]
}
```

---

## ⭐ Favoris

### `GET /favorites/`
**Voir les favoris utilisateur**  
🔐 Requiert un token

### `POST /favorites/`
**Ajouter un favori**  
🔐 Requiert un token

#### Body :
```json
{
  "destination": "Rome",
  "start_date": "2025-09-01",
  "end_date": "2025-09-05",
  "itinerary": {...},
  "flights": {...}
}
```

### `DELETE /favorites/{id}`
**Supprimer un favori**  
🔐 Requiert un token

---

## 🛠 Admin

### `GET /admin/data`
**Récupère feedbacks, favoris, messages**  
🔐 Requiert un token **admin**

#### Réponse :
```json
{
  "feedbacks": [...],
  "favorites": [...],
  "support": [...]
}
```

---