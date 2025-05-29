import httpx
import os
import asyncio
import logging
from utils.signature import generate_signature
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

FLIGHT_API_URL = "https://api.travelpayouts.com/v1/flight_search"
FLIGHT_RESULT_URL = "https://api.travelpayouts.com/v1/flight_search_results?uuid="


async def fetch_flights(flight, user_ip):
    headers = {"Content-Type": "application/json"}

    API_MARKER = os.getenv("FLIGHT_API_MARKER")
    HOST = os.getenv("HOST", "traveloo.fr")

    payload = {
        "marker": API_MARKER,
        "host": HOST,
        "user_ip": user_ip,
        "locale": "fr",
        "trip_class": flight.class_,
        "passengers": {
            "adults": flight.adults,
            "children": flight.children,
            "infants": flight.infants,
        },
        "segments": [
            {
                "origin": flight.origin,
                "destination": flight.destination,
                "date": flight.departure_date,
            }
        ],
    }

    if flight.return_date:
        payload["segments"].append(
            {
                "origin": flight.destination,
                "destination": flight.origin,
                "date": flight.return_date,
            }
        )

    payload["signature"] = generate_signature(payload)
    
    payload["segments"] = [
        {**segment, "date": str(segment["date"])} for segment in payload["segments"]
    ]

    async with httpx.AsyncClient(timeout=15.0) as client:
        res = await client.post(FLIGHT_API_URL, json=payload, headers=headers)
        if res.status_code != 200:
            return {
                "error": "Flight API call failed",
                "status_code": res.status_code,
                "body": res.text,
            }

        try:
            data = res.json()
        except Exception:
            return {"error": "Invalid JSON response from flight API", "body": res.text}

        search_id = data.get("search_id")
        if not search_id:
            return {"error": "Flight search init failed", "response": data}

        logger.info("🔎 search_id reçu : %s", search_id)
        logger.info("⏳ Attente de 3 secondes pour que les résultats soient prêts...")
        await asyncio.sleep(3)

        # Appel auto pour récupérer les résultats
        result_res = await client.get(FLIGHT_RESULT_URL + search_id)
        if result_res.status_code != 200:
            return {
                "error": "Flight results fetch failed",
                "status_code": result_res.status_code,
                "body": result_res.text,
            }

        try:
            return result_res.json()
        except Exception:
            return {"error": "Invalid JSON response from flight results", "body": result_res.text}
