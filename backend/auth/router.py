
# Import the Pydantic models needed in this router file
from backend.auth.models.user import UserCreate, User # <--- ADD THIS LINE
# You might also need User, UserUpdate, or UserLogin depending on your routes.

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import timedelta
from backend.auth.models.user import User
from backend.auth.services.auth_service import AuthService
from backend.database import get_db

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: User

@router.post("/auth/login", response_model=TokenResponse)
async def login(req: LoginRequest, auth_service: AuthService = Depends(AuthService)):
    user = auth_service.get_user_by_username(req.username)
    if not user or not auth_service.verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=30)
    access_token = auth_service.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    # Update last login
    user = auth_service.update_last_login(user)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.post("/auth/register")
async def register(user: UserCreate, auth_service: AuthService = Depends(AuthService)):
    db_user = auth_service.get_user_by_username(user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    db_user = auth_service.get_user_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return auth_service.create_user(user)

@router.get("/auth/me")
async def get_current_user(current_user: User = Depends(AuthService.get_current_user)):
    return current_user
