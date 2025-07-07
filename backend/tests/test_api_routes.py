import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient
from backend.main import app
from pathlib import Path


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


def test_new_reflexion_endpoint():
    client = TestClient(app)
    payload = {"test_log": "err", "code_snippet": "x", "context": {}}
    resp = client.post("/reflexion", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "plan" in data and "snapshot_id" in data


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


def test_export_frontend_download(monkeypatch, tmp_path: Path):
    client = TestClient(app)
    frontend = tmp_path / "frontend"
    frontend.mkdir()
    (frontend / "index.html").write_text("hi")
    monkeypatch.setattr(
        ExporterAgent,
        "export",
        lambda self, p: str(frontend.with_suffix(".zip")),
    )
    resp = client.get("/export/frontend")
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/octet-stream"


def test_monetizer_route(monkeypatch):
    monkeypatch.setattr(
        "backend.agents.monetizer_agent.stripe.Charge.create", lambda **kw: None
    )
    monkeypatch.setenv("STRIPE_API_KEY", "sk_test")
    client = TestClient(app)
    resp = client.post("/monetizer/charge", json={"user_id": "cus_1", "amount": 100})
    assert resp.status_code == 200
    assert resp.json()["status"] == "charged"


def test_checkout_route(monkeypatch):
    class Session:
        def __init__(self, url="http://checkout"):
            self.url = url

    import types
    import backend.monetizer_agent as mod

    checkout = types.SimpleNamespace(
        Session=types.SimpleNamespace(create=lambda **kw: Session())
    )
    monkeypatch.setattr(mod, "stripe", types.SimpleNamespace(checkout=checkout))
    monkeypatch.setenv("STRIPE_SECRET_KEY", "sk")
    monkeypatch.setenv("STRIPE_PRICE_STARTER", "price1")
    monkeypatch.setenv("STRIPE_PRICE_PRO", "price2")
    monkeypatch.setenv("STRIPE_PRICE_ENTERPRISE", "price3")
    monkeypatch.setenv("FRONTEND_URL", "http://frontend")

    client = TestClient(app)
    resp = client.post(
        "/charge",
        json={"user_id": "cus_1", "plan": "starter", "email": "a@b.com"},
    )
    assert resp.status_code == 200
    assert resp.json()["checkout_url"] == "http://checkout"
