from fastapi.testclient import TestClient
from backend.main import app
from backend.security import _verify_jwt


def test_login_success():
    client = TestClient(app)
    resp = client.post("/auth/login", json={"username": "free", "password": "freepass"})
    assert resp.status_code == 200
    token = resp.json()["token"]
    payload = _verify_jwt(token)
    assert payload["user"] == "free"
    assert payload["role"] == "freetier"


def test_login_invalid():
    client = TestClient(app)
    resp = client.post("/auth/login", json={"username": "free", "password": "wrong"})
    assert resp.status_code == 401
