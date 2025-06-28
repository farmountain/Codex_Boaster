import pytest
fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient
from backend.main import app


def test_chat_endpoint():
    client = TestClient(app)
    payload = {"session_id": "s1", "messages": [{"role": "user", "content": "plan my app"}]}
    resp = client.post("/chat", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "reply" in data and "agent" in data and "snapshot_id" in data
