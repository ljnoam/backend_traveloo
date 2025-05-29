import datetime
from typing import List
import google.generativeai as genai
import os
import json
import re
import logging
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

logger = logging.getLogger(__name__)

def build_gemini_prompt(city: str, start_date: str, end_date: str, profile: str, preferences: List[str]) -> str:
    prefs = ', '.join(preferences)
    base_prompt = """
Tu es un assistant de voyage expert.

L'utilisateur prévoit un voyage à {city} du {start_date} au {end_date}. Voici son profil : {profile}. Ses préférences : {prefs}.

Ta tâche : générer un **itinéraire ultra-personnalisé** jour par jour, au **format JSON uniquement**.

### Objectif :
Propose un programme riche, local et varié, qui mixe classiques incontournables et pépites moins connues.

### Contraintes à respecter :

1. **3 à 6 activités par jour**, bien réparties :
   - Matin : visite, balade ou brunch
   - Midi : **restaurant réel et bien noté** (ou brunch si pas encore fait)
   - Après-midi : visite, expérience ou shopping
   - Soir : activité détente (croisière, rooftop, bar, spectacle…) ou dîner
   - Certains jours peuvent inclure une **pause libre** ou une **activité lente** (slow travel vibes)

2. **Diversifie les types d'activités** :
   - `visit`, `walk`, `restaurant`, `experience`, `shop`, `market`, `creative_workshop`, `brunch`, `tea_time`

3. Pour chaque activité, fournis :
   - "type"
   - "name" (**nom réel** uniquement, sans commentaires ni tirets)
   - "start_time" et "end_time" au format HH:MM

4. Ne jamais ajouter de texte inutile :
   - Pas de descriptions ou commentaires dans "name"
   - Pas d'intros ou de conclusions hors JSON

5. **Exemples d'activités originales à considérer** (si pertinent) :
   - Marchés locaux, librairies, salons de thé, jardins secrets, friperies, rooftops, galeries cachées, ateliers (parfum, photo, céramique...), cours de cuisine, etc.

6. Tu peux intégrer une **journée thématique** (ex : art, détente, royal, food tour…)

### Format strictement attendu :

```json
{{  
  "city": "Paris",
  "start_date": "2025-07-15",
  "end_date": "2025-07-20",
  "days": [
    {{
      "date": "2025-07-15",
      "activities": [
        {{
          "type": "visit",
          "name": "Musée du Louvre",
          "start_time": "09:00",
          "end_time": "11:30"
        }},
        {{
          "type": "restaurant",
          "name": "Le Fumoir",
          "start_time": "12:00",
          "end_time": "13:30"
        }}
      ]
    }}
  ]
}}
```

Strictement **aucun** texte avant ou après le JSON.
"""
    return base_prompt.format(city=city, start_date=start_date, end_date=end_date, profile=profile, prefs=prefs)

# Appel à Gemini
def call_gemini_itinerary_prompt(city: str, start_date: str, end_date: str, profile: str, preferences: List[str]):
    prompt = build_gemini_prompt(city, start_date, end_date, profile, preferences)
    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
    response = model.generate_content(prompt)
    raw_text = response.text.strip()

    try:
        match = re.search(r"\{.*\}", raw_text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        else:
            raise ValueError("Aucun JSON détecté dans la réponse de Gemini.")
    except Exception as e:
        logger.error("Erreur Gemini: %s", e)
        logger.error("Réponse brute Gemini:\n%s", raw_text)
        raise

# Génération de l'itinéraire
async def generate_itinerary(city: str, start_date: str, end_date: str, profile: str, preferences: List[str]):
    raw_result = call_gemini_itinerary_prompt(city, start_date, end_date, profile, preferences)
    return raw_result