from fastapi.testclient import TestClient
from backend.main import app


def test_builder_returns_files_list():
    client = TestClient(app)
    instructions = [{
        'file_name': 'main.py',
        'purpose': 'demo',
        'language': 'python',
        'context': ''
    }]
    resp = client.post('/builder', json=instructions)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data['files'], list)
    assert data['files'][0]['language'] == 'python'
    assert 'content' in data['files'][0]
