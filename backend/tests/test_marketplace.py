import pytest
fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient
from backend.main import app


def test_marketplace_list():
    client = TestClient(app)
    resp = client.get("/marketplace/list")
    assert resp.status_code == 200
    data = resp.json()
    assert "components" in data
    assert isinstance(data["components"], list)
    assert any(c["name"] == "Ollama LLM" for c in data["components"])
