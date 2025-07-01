from fastapi.testclient import TestClient
from backend.main import app


def test_get_env_vars(tmp_path, monkeypatch):
    client = TestClient(app)
    env_file = tmp_path / ".env"
    env_file.write_text("A=1\nB=2\n#C=3\n")
    monkeypatch.setattr('backend.config_agent.ENV_FILE', str(env_file))
    resp = client.get('/api/config/env')
    assert resp.status_code == 200
    data = resp.json()
    assert {'key': 'A', 'value': '1'} in data
    assert {'key': 'B', 'value': '2'} in data
    assert all(item['key'] != 'C' for item in data)


def test_write_env_vars(tmp_path, monkeypatch):
    client = TestClient(app)
    env_file = tmp_path / '.env'
    monkeypatch.setattr('backend.config_agent.ENV_FILE', str(env_file))
    resp = client.post('/api/config/env', json={'env': [{'key': 'X', 'value': 'y'}]})
    assert resp.status_code == 200
    assert env_file.read_text() == 'X=y\n'
