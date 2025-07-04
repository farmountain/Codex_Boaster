from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.security import generate_jwt

router = APIRouter()

_USERS = {
    "free": {"password": "freepass", "role": "freetier"},
    "sub": {"password": "subpass", "role": "subscriber"},
    "enterprise": {"password": "enterpass", "role": "enterprise"},
}


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    token: str


@router.post("/auth/login", response_model=TokenResponse)
async def login(req: LoginRequest):
    user = _USERS.get(req.username)
    if not user or user["password"] != req.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = generate_jwt({"user": req.username, "role": user["role"]})
    return {"token": token}
