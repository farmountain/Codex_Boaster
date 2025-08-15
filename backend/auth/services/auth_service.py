from typing import Optional, Dict
from ...security import generate_jwt


class AuthService:
    """Simple in-memory authentication service for tests."""

    _USERS: Dict[str, Dict[str, str]] = {
        "free": {"password": "freepass", "role": "freetier"}
    }

    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, str]]:
        user = self._USERS.get(username)
        if user and user["password"] == password:
            return {"username": username, "role": user["role"]}
        return None

    def create_token(self, user: Dict[str, str]) -> str:
        return generate_jwt({"user": user["username"], "role": user["role"]})
