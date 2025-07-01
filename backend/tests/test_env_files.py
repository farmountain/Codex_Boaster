import json
from fastapi.testclient import TestClient
from backend.main import app


def test_configure_env_writes_files(tmp_path, monkeypatch):
    client = TestClient(app)

    monkeypatch.setattr('backend.config_agent.ENV_FILE', str(tmp_path / '.env'))
    monkeypatch.setattr('backend.config_agent.ENV_TEMPLATE', str(tmp_path / '.env.template.json'))
    monkeypatch.setattr('backend.config_agent.DOCKER_COMPOSE', str(tmp_path / 'docker-compose.yml'))
    monkeypatch.setattr('backend.config_agent.CONFIG_PATH', str(tmp_path / 'codexbooster.config.json'))
    monkeypatch.setattr('backend.config_agent._store_remote', lambda data: None)
    monkeypatch.setattr('backend.config_agent.store_env_snapshot', lambda d: 'snap')

    resp = client.post(
        '/configure-env',
        json={
            'runtimes': {'python': '3.11', 'node': '18', 'rust': '1.71'},
            'env_vars': {'API_KEY': '123'},
            'setup_script': [],
            'llm_services': []
        }
    )
    assert resp.status_code == 200

    assert (tmp_path / '.env').exists()
    assert (tmp_path / '.env.template.json').exists()
    assert (tmp_path / 'docker-compose.yml').exists()
    assert json.load(open(tmp_path / 'codexbooster.config.json'))['runtime']['python'] == '3.11'
