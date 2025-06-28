import pytest
fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient
from backend.main import app


def test_marketplace_list():
    client = TestClient(app)
    resp = client.get("/marketplace")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert any(item["name"] == "Ollama LLM" for item in data)


def test_marketplace_install():
    client = TestClient(app)
    item = {
        "name": "Ollama LLM",
        "type": "LLM",
        "description": "Local LLM runner with API",
        "endpoint": "http://localhost:11434",
        "icon_url": "/icons/ollama.png",
        "requires_api_key": False,
        "is_installed": False,
    }
    resp = client.post("/marketplace/install", json=item)
    assert resp.status_code == 200
    assert resp.json()["message"] == "Ollama LLM installed."
