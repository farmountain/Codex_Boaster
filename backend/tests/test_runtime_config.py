import json
from fastapi.testclient import TestClient
from backend.main import app


def test_get_runtime_config_defaults(tmp_path, monkeypatch):
    client = TestClient(app)
    monkeypatch.setattr('backend.config_agent.CONFIG_PATH', str(tmp_path / "cfg.json"))
    resp = client.get('/runtime-config')
    assert resp.status_code == 200
    body = resp.json()
    assert body['python'] == '3.12'
    assert body['nodejs'] == '20'
    assert body['ruby'] == '3.4.4'
    assert body['rust'] == '1.87.0'


def test_save_runtime_config(tmp_path, monkeypatch):
    client = TestClient(app)
    cfg = tmp_path / 'cfg.json'
    monkeypatch.setattr('backend.config_agent.CONFIG_PATH', str(cfg))
    monkeypatch.setattr('backend.config_agent.set_runtime_context', lambda d: None)
    resp = client.post('/runtime-config', json={
        'python': '3.12',
        'nodejs': '20',
        'ruby': '3.4.4',
        'rust': '1.87.0',
        'go': '1.23.8',
        'bun': '1.2.14',
        'java': '21',
        'swift': '6.1'
    })
    assert resp.status_code == 200
    assert resp.json()['message'] == 'Runtime config saved.'
    data = json.load(cfg.open())
    assert data['runtime']['python'] == '3.12'

def test_set_single_runtime(tmp_path, monkeypatch):
    client = TestClient(app)
    cfg = tmp_path / 'cfg.json'
    monkeypatch.setattr('backend.config_agent.CONFIG_PATH', str(cfg))
    monkeypatch.setattr('backend.config_agent.set_runtime_context', lambda d: None)
    resp = client.post('/api/config/runtime', json={'language': 'Python', 'version': '3.8'})
    assert resp.status_code == 200
    data = json.load(cfg.open())
    assert data['runtime']['python'] == '3.8'
