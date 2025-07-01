import pytest
fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient
from backend.main import app


def test_chat_endpoint():
    client = TestClient(app)
    payload = {
        "session_id": "s1",
        "message": "plan my app",
        "history": [],
    }
    resp = client.post("/api/chat", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert {
        "response",
        "actions",
        "reflexion_summary",
        "memory_log",
        "snapshot_id",
    }.issubset(data.keys())
