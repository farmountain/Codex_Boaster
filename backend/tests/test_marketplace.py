import pytest
fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient
from backend.main import app
import backend.marketplace as marketplace


def test_register_and_list_plugin(tmp_path, monkeypatch):
    store = tmp_path / "plugins.json"
    monkeypatch.setattr(marketplace, "PLUGIN_STORE", str(store))
    client = TestClient(app)

    plugin = {
        "plugin_id": "test-plugin-1",
        "name": "Test Plugin",
        "type": "LLM",
        "entrypoint": "http://localhost:1234",
        "capabilities": ["test"],
        "version": "1.0.0",
    }

    resp = client.post("/api/marketplace/register", json=plugin)
    assert resp.status_code == 200
    assert resp.json()["status"] == "success"

    resp = client.get("/api/marketplace")
    assert resp.status_code == 200
    data = resp.json()
    assert any(p["plugin_id"] == plugin["plugin_id"] for p in data)


def test_toggle_plugin(tmp_path, monkeypatch):
    store = tmp_path / "plugins.json"
    monkeypatch.setattr(marketplace, "PLUGIN_STORE", str(store))
    client = TestClient(app)

    plugin = {
        "plugin_id": "test-plugin-2",
        "name": "Toggle Plugin",
        "type": "Database",
        "entrypoint": "http://localhost:5678",
        "capabilities": ["toggle"],
        "version": "0.1.0",
    }

    client.post("/api/marketplace/register", json=plugin)
    resp = client.post(f"/api/marketplace/toggle/{plugin['plugin_id']}")
    assert resp.status_code == 200
    assert resp.json()["enabled"] is False

    resp = client.get("/api/marketplace")
    assert resp.json()[0]["enabled"] is False
