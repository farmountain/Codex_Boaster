"""Authentication and rate limiting utilities."""

import base64
import hmac
import json
import os
import time
from collections import defaultdict
from hashlib import sha256
from typing import Callable

from fastapi import Depends, HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

JWT_SECRET_KEY = os.getenv("JWT_SECRET", "secret")
JWT_ALGORITHM = "HS256" # Added this line
RATE_LIMIT = int(os.getenv("RATE_LIMIT", "60"))
RATE_WINDOW = int(os.getenv("RATE_WINDOW", "60"))

_request_log: defaultdict[str, list[float]] = defaultdict(list)


def generate_jwt(payload: dict) -> str:
    """Create a signed JWT for the given payload."""
    header_b64 = base64.urlsafe_b64encode(
        json.dumps({"alg": "HS256", "typ": "JWT"}).encode()
    ).rstrip(b"=").decode()
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).rstrip(
        b"="
    ).decode()
    signature = base64.urlsafe_b64encode(
        hmac.new(SECRET_KEY.encode(), f"{header_b64}.{payload_b64}".encode(), sha256).digest()
    ).rstrip(b"=").decode()
    return f"{header_b64}.{payload_b64}.{signature}"


def _verify_jwt(token: str) -> dict:
    try:
        header_b64, payload_b64, signature = token.split(".")
        data = f"{header_b64}.{payload_b64}".encode()
        expected = base64.urlsafe_b64encode(
            hmac.new(SECRET_KEY.encode(), data, sha256).digest()
        ).rstrip(b"=").decode()
        if not hmac.compare_digest(expected, signature):
            raise ValueError("signature mismatch")
        payload_json = base64.urlsafe_b64decode(payload_b64 + "==").decode()
        return json.loads(payload_json)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token") from e


async def require_auth(request: Request) -> dict:
    auth = request.headers.get("Authorization")
    if not auth:
        raise HTTPException(status_code=401, detail="Missing token")
    token = auth.split()[-1]
    payload = _verify_jwt(token)
    _enforce_rate_limit(request.client.host)
    request.state.user = payload
    return payload


def _enforce_rate_limit(key: str) -> None:
    now = time.time()
    history = _request_log[key]
    history[:] = [t for t in history if now - t < RATE_WINDOW]
    if len(history) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    history.append(now)


def require_role(role: str) -> Callable:
    async def _wrapper(payload: dict = Depends(require_auth)):
        if payload.get("role") != role:
            raise HTTPException(status_code=403, detail="Insufficient privileges")
    return _wrapper


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            await require_auth(request)
        except HTTPException as exc:  # pragma: no cover - auth failure
            return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)
        return await call_next(request)
