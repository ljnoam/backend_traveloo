from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, EmailStr
from typing import Optional
from services.auth import (
    login_user,
    register_user,
    get_user_profile_from_token,
    update_user_profile
)

router = APIRouter(prefix="/auth")
oauth2_scheme = APIKeyHeader(name="Authorization")


class AuthPayload(BaseModel):
    email: EmailStr
    password: str


class ProfileUpdate(BaseModel):
    full_name: Optional[str]
    avatar_url: Optional[str]


@router.post("/login")
def login(data: AuthPayload):
    try:
        return login_user(data.email, data.password)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/register")
def register(data: AuthPayload):
    try:
        return register_user(data.email, data.password)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/me")
def me(token: str = Depends(oauth2_scheme)):
    try:
        if token.startswith("Bearer "):
            token = token.replace("Bearer ", "")
        return get_user_profile_from_token(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.put("/update-profile")
def update_profile(payload: ProfileUpdate, token: str = Depends(oauth2_scheme)):
    try:
        if token.startswith("Bearer "):
            token = token.replace("Bearer ", "")
        return update_user_profile(token, payload.dict(exclude_unset=True))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
