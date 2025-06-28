from fastapi.testclient import TestClient
from backend.main import app
import backend.terminal_runner as tr


def test_run_setup_script_multiple_commands(tmp_path, monkeypatch):
    client = TestClient(app)
    monkeypatch.setattr(tr, "LOG_DIR", tmp_path)
    resp = client.post("/run-setup", json={"commands": ["echo hi", "echo world"]})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["results"]) == 2
    assert all(r["status"] == "success" for r in data["results"])
    assert any(tmp_path.iterdir())


