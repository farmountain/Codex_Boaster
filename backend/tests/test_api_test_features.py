import pytest
from fastapi.testclient import TestClient
from backend.main import app

fastapi = pytest.importorskip("fastapi")


def test_run_tests_endpoint(monkeypatch):
    client = TestClient(app)

    class Result:
        def __init__(self):
            self.stdout = "ok"
            self.stderr = ""
            self.returncode = 0

    monkeypatch.setattr('backend.tester_agent.subprocess.run', lambda *a, **k: Result())

    resp = client.post("/run-tests", json={"runtime": "python"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["snapshot_id"]


def test_generate_tests_endpoint(monkeypatch):
    client = TestClient(app)
    monkeypatch.setattr('backend.test_suite_agent.generate_test_cases', lambda code, t: "tests")
    resp = client.post(
        "/generate-tests",
        json={"file_name": "mod.py", "code": "print(1)", "test_type": "unit"},
    )
    assert resp.status_code == 200
    assert resp.json()["test_code"] == "tests"
