import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient
from backend.main import app


def test_build_and_test_route():
    client = TestClient(app)
    tests = """from generated_module import add


def test_add():
    assert add(1,2) == 3
"""
    resp = client.post("/builder/build_and_test", json={"tests": tests})
    assert resp.status_code == 200
    data = resp.json()
    assert "code" in data
    assert data["success"] is True
