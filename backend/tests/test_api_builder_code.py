import pytest
from fastapi.testclient import TestClient
from backend.main import app


fastapi = pytest.importorskip("fastapi")

def test_builder_code_endpoint(monkeypatch):
    client = TestClient(app)
    monkeypatch.setattr('backend.llm_client.generate_code_snippet', lambda *a, **k: 'print(1)')
    instructions = [{
        'file_name': 'main.py',
        'purpose': 'demo',
        'language': 'python',
        'context': ''
    }]
    resp = client.post('/builder', json=instructions)
    assert resp.status_code == 200
    data = resp.json()
    assert data['status'] == 'ok'
    assert data['files'][0]['file_name'] == 'main.py'
    assert 'snapshot_id' in data
