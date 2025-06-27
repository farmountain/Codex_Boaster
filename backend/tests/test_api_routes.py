import pytest
fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient
from backend.main import app


def test_builder_route():
    client = TestClient(app)
    tests = """from generated_module import add


def test_add():
    assert add(1,2) == 3
"""
    resp = client.post("/builder/build", json={"tests": tests})
    assert resp.status_code == 200
    data = resp.json()
    assert "code" in data


def test_builder_root_route():
    client = TestClient(app)
    tests = """from generated_module import add


def test_add():
    assert add(1,2) == 3
"""
    resp = client.post("/build", json={"tests": tests})
    assert resp.status_code == 200
    data = resp.json()
    assert "code" in data


def test_tester_route():
    client = TestClient(app)
    code = "def add(a, b):\n    return a + b\n"
    tests = """from generated_module import add


def test_add():
    assert add(1,2) == 3
"""
    resp = client.post("/tester/run", json={"code": code, "tests": tests})
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert "output" in data


def test_tester_root_route():
    client = TestClient(app)
    code = "def add(a, b):\n    return a + b\n"
    tests = """from generated_module import add


def test_add():
    assert add(1,2) == 3
"""
    resp = client.post("/test", json={"code": code, "tests": tests})
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert "output" in data


def test_reflexion_route():
    client = TestClient(app)
    resp = client.post("/reflexion/reflect", json={"feedback": "failed"})
    assert resp.status_code == 200
    assert "instructions" in resp.json()


def test_reflexion_root_route():
    client = TestClient(app)
    resp = client.post("/reflect", json={"feedback": "failed"})
    assert resp.status_code == 200
    assert "instructions" in resp.json()


def test_exporter_route(tmp_path):
    client = TestClient(app)
    src = tmp_path / "src"
    src.mkdir()
    (src / "file.txt").write_text("a")
    resp = client.post("/exporter/export", json={"path": str(src)})
    assert resp.status_code == 200
    archive = resp.json()["archive"]
    assert archive.endswith(".zip")


def test_exporter_root_route(tmp_path):
    client = TestClient(app)
    src = tmp_path / "src"
    src.mkdir()
    (src / "file.txt").write_text("a")
    resp = client.post("/export", json={"path": str(src)})
    assert resp.status_code == 200
    archive = resp.json()["archive"]
    assert archive.endswith(".zip")


def test_monetizer_route(monkeypatch):
    monkeypatch.setattr(
        "backend.agents.monetizer_agent.stripe.Charge.create", lambda **kw: None
    )
    monkeypatch.setenv("STRIPE_API_KEY", "sk_test")
    client = TestClient(app)
    resp = client.post("/monetizer/charge", json={"user_id": "cus_1", "amount": 100})
    assert resp.status_code == 200
    assert resp.json()["status"] == "charged"


def test_monetizer_root_route(monkeypatch):
    monkeypatch.setattr(
        "backend.agents.monetizer_agent.stripe.Charge.create", lambda **kw: None
    )
    monkeypatch.setenv("STRIPE_API_KEY", "sk_test")
    client = TestClient(app)
    resp = client.post("/charge", json={"user_id": "cus_1", "amount": 100})
    assert resp.status_code == 200
    assert resp.json()["status"] == "charged"
