import pytest
from fastapi.testclient import TestClient
from backend.main import app
import backend.hipcortex_bridge as bridge

fastapi = pytest.importorskip("fastapi")

def test_memory_log_endpoint(monkeypatch, tmp_path):
    monkeypatch.setattr(bridge, "LOG_DIR", tmp_path)
    client = TestClient(app)
    payload1 = {
        "session_id": "s1",
        "agent": "ReflexionAgent",
        "step": "plan",
        "content": "c1",
        "confidence": 0.5,
        "timestamp": "2025-01-01T00:00:00Z"
    }
    payload2 = {
        "session_id": "s1",
        "agent": "ReflexionAgent",
        "step": "revise",
        "content": "c2",
        "confidence": 0.6,
        "timestamp": "2025-01-01T00:00:01Z"
    }
    client.post("/api/hipcortex/record", json=payload1)
    client.post("/api/hipcortex/record", json=payload2)

    logs = client.get("/api/hipcortex/memory-log", params={"session_id": "s1"})
    assert logs.status_code == 200
    data = logs.json()
    assert len(data) == 2
    assert data[0]["step"] == "plan"
    assert data[1]["step"] == "revise"
