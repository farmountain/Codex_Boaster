import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient
from backend.main import app


def test_docs_route():
    client = TestClient(app)
    payload = {"project_name": "demo"}
    resp = client.post("/api/docs", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("status") == "success"
    assert "markdown" in data
