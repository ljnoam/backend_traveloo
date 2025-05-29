# routes/admin.py
from fastapi import APIRouter, Depends
from services.auth import require_admin
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/data")
def get_admin_data(admin=Depends(require_admin)):
    favorites = supabase.table("favorites").select("*").execute().data or []
    feedbacks = supabase.table("feedbacks").select("*").execute().data or []
    support = supabase.table("support").select("*").execute().data or []

    return {
        "favorites": favorites,
        "feedbacks": feedbacks,
        "support_messages": support
    }
