# services/auth.py
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from datetime import datetime
from fastapi.security import APIKeyHeader
from fastapi import Depends, HTTPException

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

auth_header = APIKeyHeader(name="Authorization")


def login_user(email: str, password: str):
    res = supabase.auth.sign_in_with_password({"email": email, "password": password})
    if res.user is None or res.session is None:
        raise Exception("Login failed: identifiants invalides ou compte non confirmé.")

    user_id = res.user.id
    now = datetime.utcnow().isoformat()
    supabase.table("profiles").update({"last_login": now}).eq("id", user_id).execute()

    return res


def register_user(email: str, password: str):
    res = supabase.auth.sign_up({"email": email, "password": password})
    if "error" in res and res["error"]:
        raise Exception(res["error"]["message"])
    return res


def get_user_profile_from_token(token: str):
    if token.startswith("Bearer "):
        token = token.replace("Bearer ", "")
    session = supabase.auth.get_user(token)
    user_id = session.user.id

    profile = supabase.table("profiles").select("*").eq("id", user_id).single().execute()
    if "error" in profile and profile["error"]:
        raise Exception("Profil non trouvé")
    return profile.data


def update_user_profile(token: str, data: dict):
    if token.startswith("Bearer "):
        token = token.replace("Bearer ", "")
    session = supabase.auth.get_user(token)
    user_id = session.user.id

    result = supabase.table("profiles").update(data).eq("id", user_id).execute()
    if "error" in result and result["error"]:
        raise Exception("Erreur mise à jour profil")
    return result.data


def get_authenticated_user(token: str = Depends(auth_header)):
    return get_user_profile_from_token(token)


def require_admin(user=Depends(get_authenticated_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Accès réservé aux administrateurs")
    return user
