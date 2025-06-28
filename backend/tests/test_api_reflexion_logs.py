import pytest
fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient
from backend.main import app


def test_reflexion_logs_endpoint():
    client = TestClient(app)
    resp = client.get("/reflexion/logs")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    assert {"timestamp", "agent", "confidence", "suggestion", "log"}.issubset(data[0])
