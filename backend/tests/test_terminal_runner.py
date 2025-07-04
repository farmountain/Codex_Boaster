from fastapi.testclient import TestClient
from backend.main import app
import backend.terminal_runner as tr
from backend.security import generate_jwt


def test_run_single_command_requires_auth(tmp_path, monkeypatch):
    client = TestClient(app)
    monkeypatch.setattr(tr, "LOG_DIR", tmp_path)
    resp = client.post("/api/run-setup", json={"command": "echo hello"})
    assert resp.status_code == 401


def test_run_single_command_success(tmp_path, monkeypatch):
    client = TestClient(app)
    monkeypatch.setattr(tr, "LOG_DIR", tmp_path)
    token = generate_jwt({"role": "admin"})
    resp = client.post(
        "/api/run-setup",
        json={"command": "echo hello"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["stdout"].strip() == "hello"
    assert data["exit_code"] == 0
    assert (tmp_path / f"{data['log_id']}.log").exists()


def test_run_single_command_disallowed(tmp_path, monkeypatch):
    client = TestClient(app)
    monkeypatch.setattr(tr, "LOG_DIR", tmp_path)
    token = generate_jwt({"role": "admin"})
    resp = client.post(
        "/api/run-setup",
        json={"command": "rm -rf /"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 403


