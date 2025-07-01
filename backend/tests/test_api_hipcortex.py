import json
import pytest
from fastapi.testclient import TestClient
from backend.main import app
import backend.hipcortex_bridge as bridge

fastapi = pytest.importorskip("fastapi")

def test_record_logs_and_rollback(monkeypatch, tmp_path):
    monkeypatch.setattr(bridge, "LOG_DIR", tmp_path)
    client = TestClient(app)
    payload1 = {
        "session_id": "s1",
        "agent": "ArchitectAgent",
        "step": "Plan",
        "content": "first plan",
        "confidence": 0.9,
    }
    payload2 = {
        "session_id": "s1",
        "agent": "BuilderAgent",
        "step": "Build",
        "content": "second step",
        "confidence": 0.8,
    }
    resp1 = client.post("/api/hipcortex/record", json=payload1)
    assert resp1.status_code == 200
    assert resp1.json()["version"] == "v1"
    resp2 = client.post("/api/hipcortex/record", json=payload2)
    assert resp2.status_code == 200
    assert resp2.json()["version"] == "v2"

    logs = client.get("/api/hipcortex/logs", params={"session_id": "s1"}).json()
    assert [v["version"] for v in logs] == ["v1", "v2"]

    # rollback to v1
    rb = client.post("/api/hipcortex/rollback", json={"session_id": "s1", "target_version": "v1"})
    assert rb.status_code == 200
    data = json.load(open(tmp_path / "s1.json"))
    assert data["current_version"] == "v1"

    # query sessions by confidence
    q = client.get("/api/hipcortex/query", params={"confidence_lt": 0.85})
    assert q.status_code == 200
    assert "s1" in q.json()
