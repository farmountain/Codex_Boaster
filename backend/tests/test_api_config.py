import pytest
fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient
from backend.main import app


def test_configure_env(monkeypatch):
    client = TestClient(app)
    called = {}

    def fake_store(data):
        called['data'] = data
        return 'snap123'

    monkeypatch.setattr('backend.config_agent.store_env_snapshot', fake_store)

    resp = client.post(
        '/configure-env',
        json={
            'runtimes': {'python': '3.12'},
            'env_vars': {'OPENAI_API_KEY': 'sk-test'},
            'setup_script': ['echo ok']
        }
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body['snapshot_id'] == 'snap123'
    assert called['data']['runtimes']['python'] == '3.12'
