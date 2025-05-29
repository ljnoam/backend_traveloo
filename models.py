from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date  # ✅ Ajout pour typage des dates


class FlightInfo(BaseModel):
    origin: str
    destination: str
    departure_date: date  # ✅ modifié
    return_date: Optional[date] = None  # ✅ modifié
    class_: str
    adults: int
    children: int
    infants: int


class ItineraryRequest(BaseModel):
    city: str
    start_date: date  # ✅ modifié
    end_date: date  # ✅ modifié
    profile: str
    preferences: List[str]


class FavoriteCreate(BaseModel):
    destination: str
    start_date: date  # ✅ modifié
    end_date: date  # ✅ modifié
    itinerary: dict
    flights: dict


class FeedbackCreate(BaseModel):
    message: str


class SupportMessage(BaseModel):
    nom: str
    email: EmailStr
    sujet: str
    message: str


class AuthPayload(BaseModel):
    email: EmailStr
    password: str


class ProfileUpdate(BaseModel):
    full_name: Optional[str]
    avatar_url: Optional[str]
