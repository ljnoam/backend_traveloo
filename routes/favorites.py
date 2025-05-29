# routes/favorites.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from services.auth import get_authenticated_user, require_admin
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

router = APIRouter(prefix="/favorites", tags=["favorites"])


class FavoriteCreate(BaseModel):
    destination: str
    start_date: str
    end_date: str
    itinerary: dict
    flights: dict
    hotels: dict


@router.get("/")
def get_my_favorites(user=Depends(get_authenticated_user)):
    response = supabase.table("favorites").select("*").eq("user_id", user["id"]).execute()
    return response.data or []


@router.post("/")
def add_favorite(payload: FavoriteCreate, user=Depends(get_authenticated_user)):
    data = {
        "user_id": user["id"],
        **payload.dict()
    }
    res = supabase.table("favorites").insert(data).execute()
    return res.data[0] if res.data else {"message": "Erreur insertion"}


@router.delete("/{favorite_id}")
def delete_favorite(favorite_id: int, user=Depends(get_authenticated_user)):
    check = supabase.table("favorites").select("*").eq("id", favorite_id).eq("user_id", user["id"]).single().execute()
    if check.data is None:
        raise HTTPException(status_code=404, detail="Favori introuvable ou accès refusé")
    supabase.table("favorites").delete().eq("id", favorite_id).execute()
    return {"message": "Favori supprimé"}


@router.get("/admin/all")
def get_all_favorites(admin=Depends(require_admin)):
    response = supabase.table("favorites").select("*").execute()
    return response.data or []
