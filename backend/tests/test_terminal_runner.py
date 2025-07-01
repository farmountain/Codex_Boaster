from fastapi.testclient import TestClient
from backend.main import app
import backend.terminal_runner as tr


def test_run_single_command(tmp_path, monkeypatch):
    client = TestClient(app)
    monkeypatch.setattr(tr, "LOG_DIR", tmp_path)
    resp = client.post("/api/run-setup", json={"command": "echo hello"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["stdout"].strip() == "hello"
    assert data["exit_code"] == 0
    assert (tmp_path / f"{data['log_id']}.log").exists()


