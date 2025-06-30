from fastapi.testclient import TestClient
from backend.main import app


def test_deploy_vercel_success(monkeypatch):
    client = TestClient(app)

    class Res:
        def raise_for_status(self):
            pass

        def json(self):
            return {"url": "demo.vercel.app"}

    monkeypatch.setattr("backend.deploy_agent.requests.post", lambda *a, **k: Res())
    monkeypatch.setattr("backend.deploy_agent.get_secret", lambda name: "tok")
    monkeypatch.setattr("backend.deploy_agent.store_deploy_snapshot", lambda r: "snap123")

    resp = client.post(
        "/api/deploy",
        json={
            "project_name": "demo",
            "repo_url": "https://github.com/x/demo",
            "provider": "vercel",
            "framework": "nextjs",
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "success"
    assert body["snapshot_id"] == "snap123"
    assert body["deployment_url"] == "demo.vercel.app"


def test_deploy_unsupported_provider():
    client = TestClient(app)
    resp = client.post(
        "/api/deploy",
        json={
            "project_name": "demo",
            "repo_url": "https://github.com/x/demo",
            "provider": "unknown",
        },
    )
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Unsupported deployment provider"
