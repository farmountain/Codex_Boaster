import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient
from backend.main import app


def test_build_and_test_updates_status_and_suggestion():
    client = TestClient(app)
    failing_tests = """from generated_module import add


def test_add():
    assert add(1, 2) == 4
"""
    resp = client.post("/builder/build_and_test", json={"tests": failing_tests})
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is False

    res = client.get("/test_results")
    body = res.json()
    assert body["success"] is False
    assert "output" in body

    res = client.get("/improvement_suggestion")
    sugg = res.json()["suggestion"]
    assert sugg
    assert "coverage" in sugg or "continue" in sugg
