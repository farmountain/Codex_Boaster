from fastapi.testclient import TestClient

from backend.main import app


def test_deploy_success(monkeypatch):
    client = TestClient(app)

    class Result:
        def __init__(self):
            self.returncode = 0
            self.stdout = "done"
            self.stderr = ""

    monkeypatch.setattr(
        "backend.deploy_agent.subprocess.run", lambda *a, **k: Result()
    )
    monkeypatch.setattr(
        "backend.deploy_agent.store_deploy_snapshot", lambda r: "snap123"
    )

    resp = client.post(
        "/deploy",
        json={
            "runtime": "node",
            "platform": "vercel",
            "project_name": "demo",
            "token": "tok",
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "success"
    assert body["snapshot_id"] == "snap123"


def test_deploy_unsupported_platform():
    client = TestClient(app)
    resp = client.post(
        "/deploy",
        json={
            "runtime": "node",
            "platform": "unknown",
            "project_name": "demo",
            "token": "tok",
        },
    )
    assert resp.status_code == 200
    assert resp.json()["error"] == "Unsupported platform"

