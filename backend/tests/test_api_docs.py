import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient
from backend.main import app


def test_docs_route():
    client = TestClient(app)
    payload = {"files": {"main.py": "print('hi')"}, "context": {}}
    resp = client.post("/docs", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "documentation" in data
    assert "snapshot_id" in data
