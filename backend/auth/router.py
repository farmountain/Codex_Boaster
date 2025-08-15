from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from backend.auth.services.auth_service import AuthService

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    token: str


@router.post("/auth/login", response_model=TokenResponse)
async def login(req: LoginRequest, auth_service: AuthService = Depends(AuthService)):
    user = auth_service.authenticate_user(req.username, req.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = auth_service.create_token(user)
    return {"token": token}
