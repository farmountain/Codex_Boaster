import pytest
from fastapi.testclient import TestClient
from backend.main import app
import backend.architect_agent as arc
import backend.builder_agent as build_mod
import backend.tester_agent as test_mod
import backend.reflexion_agent as refl_mod
import backend.deploy_agent as deploy_mod
import backend.terminal_runner as term
from backend.security import generate_jwt

fastapi = pytest.importorskip("fastapi")


def test_full_multi_agent_flow(monkeypatch, tmp_path):
    client = TestClient(app)

    # collect snapshot calls
    snapshots = {}

    def mark(name, value):
        snapshots[name] = True
        return value

    monkeypatch.setattr(arc, "store_plan_snapshot", lambda *a, **k: mark("plan", "plan123"))
    monkeypatch.setattr(build_mod, "store_code_snapshot", lambda *a, **k: mark("code", "code123"))
    monkeypatch.setattr(test_mod, "store_test_results", lambda *a, **k: mark("test", "test123"))
    monkeypatch.setattr(refl_mod, "store_reflexion_snapshot", lambda *a, **k: mark("refl", "refl123"))
    monkeypatch.setattr(deploy_mod, "store_deploy_snapshot", lambda *a, **k: mark("deploy", "dep123"))

    # patch external effects
    monkeypatch.setattr("backend.llm_client.generate_code_snippet", lambda *a, **k: "def add(a,b):\n    return a + b\n")
    monkeypatch.setattr(test_mod, "subprocess", type("P", (), {"run": lambda *a, **k: type('R', (), {"stdout": "", "stderr": "", "returncode": 0})()})())
    monkeypatch.setattr(refl_mod, "generate_improvement_suggestions", lambda **kw: {"steps": ["done"], "confidence": 0.9})
    monkeypatch.setattr(refl_mod, "emit_confidence_log", lambda *a, **k: None)
    monkeypatch.setattr(refl_mod, "emit_reflexion_log", lambda *a, **k: None)

    class Res:
        def raise_for_status(self):
            pass
        def json(self):
            return {"url": "demo.vercel.app"}
    monkeypatch.setattr(deploy_mod.requests, "post", lambda *a, **kw: Res())
    monkeypatch.setattr(deploy_mod, "get_secret", lambda name: "tok")

    # Plan project
    plan = client.post("/architect", json={"prompt": "demo"})
    assert plan.status_code == 200
    assert plan.json()["plan_id"] == "plan123"

    # Build code
    instructions = [{"file_name": "main.py", "purpose": "demo", "language": "python"}]
    build = client.post("/builder", json=instructions)
    assert build.status_code == 200
    assert build.json()["snapshot_id"] == "code123"

    # Run tests
    tests = client.post("/run-tests", json={"runtime": "python"})
    assert tests.status_code == 200
    assert tests.json()["snapshot_id"] == "test123"

    # Reflexion
    ref = client.post("/reflexion", json={"test_log": "fail", "code_snippet": "x", "context": {}})
    assert ref.status_code == 200
    assert ref.json()["snapshot_id"] == "refl123"

    # Deploy
    dep = client.post("/api/deploy", json={"project_name": "demo", "repo_url": "https://github.com/x/demo", "provider": "vercel"})
    assert dep.status_code == 200
    assert dep.json()["snapshot_id"] == "dep123"

    # ensure all snapshots stored
    assert snapshots == {"plan": True, "code": True, "test": True, "refl": True, "deploy": True}


def test_deploy_missing_api_key(monkeypatch):
    client = TestClient(app)
    monkeypatch.setattr(deploy_mod, "get_secret", lambda name: None)
    resp = client.post("/api/deploy", json={"project_name": "demo", "repo_url": "https://github.com/x/demo", "provider": "vercel"})
    assert resp.status_code == 500
    assert "Missing Vercel API token" in resp.json()["detail"]


def test_terminal_runner_rbac(monkeypatch, tmp_path):
    client = TestClient(app)
    monkeypatch.setattr(term, "LOG_DIR", tmp_path)
    resp = client.post("/api/run-setup", json={"command": "echo hi"})
    assert resp.status_code == 401

    token = generate_jwt({"role": "admin"})
    monkeypatch.setattr(term, "subprocess", type("P", (), {"run": lambda *a, **k: type('R', (), {"stdout": b"hi", "stderr": b"", "returncode": 0})()})())
    resp = client.post("/api/run-setup", json={"command": "echo hi"}, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["exit_code"] == 0
