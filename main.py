import os
import logging
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from models import FlightInfo, ItineraryRequest
from services.flights import fetch_flights
from services.itinerary import generate_itinerary
from routes import favorites, admin, auth
from utils.parser_utils import parse_flights

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    docs_url=None if os.getenv("ENV") == "prod" else "/docs",
    redoc_url=None if os.getenv("ENV") == "prod" else "/redoc",
    openapi_url=None if os.getenv("ENV") == "prod" else "/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://traveloo.fr", "http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(auth.router)
app.include_router(favorites.router)
app.include_router(admin.router)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("❌ Exception non gérée : %s", exc, exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Une erreur interne est survenue. Contactez le support si ça persiste."},
    )

@app.post(
    "/api/search",
    tags=["Flights"],
    summary="Rechercher des vols",
    description="Recherche des vols via l'API TravelPayouts, avec parsing du résultat brut."
)
async def search_flight_only(flight: FlightInfo, request: Request):
    user_ip = request.client.host
    raw_result = await fetch_flights(flight, user_ip)

    if "error" in raw_result:
        return raw_result  # ne pas parser les erreurs

    parsed = parse_flights(raw_result)
    logger.info("📦 Résultat formaté des vols : %s", parsed)
    return parsed


@app.post(
    "/generate-itinerary",
    tags=["Itinerary"],
    summary="Générer un itinéraire personnalisé",
    description="Utilise l'API Gemini pour générer un planning de voyage jour par jour en fonction du profil utilisateur."
)
async def create_itinerary(request: ItineraryRequest):
    itinerary = await generate_itinerary(
        request.city,
        request.start_date,
        request.end_date,
        request.profile,
        request.preferences
    )
    return itinerary
