import json
from fastapi.testclient import TestClient
from backend.main import app


def test_get_runtime_config_defaults(tmp_path, monkeypatch):
    client = TestClient(app)
    monkeypatch.setattr('backend.config_agent.CONFIG_PATH', str(tmp_path / "cfg.json"))
    resp = client.get('/runtime-config')
    assert resp.status_code == 200
    body = resp.json()
    assert body['python'] == '3.10'
    assert body['node'] == '18'
    assert body['go'] == '1.19'


def test_save_runtime_config(tmp_path, monkeypatch):
    client = TestClient(app)
    cfg = tmp_path / 'cfg.json'
    monkeypatch.setattr('backend.config_agent.CONFIG_PATH', str(cfg))
    monkeypatch.setattr('backend.config_agent.set_runtime_context', lambda d: None)
    resp = client.post('/runtime-config', json={'python': '3.11', 'node': '20', 'go': '1.21'})
    assert resp.status_code == 200
    assert resp.json()['message'] == 'Runtime config saved.'
    data = json.load(cfg.open())
    assert data['runtime']['python'] == '3.11'
