import pytest
fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient

from backend.main import app
from backend.repo_init_agent import generate_template
import os


def make_resp(status=201, data=None):
    class R:
        def __init__(self):
            self.status_code = status
        def json(self):
            return data or {}
    return R()


def test_generate_template_python_node():
    py = generate_template("python")
    node = generate_template("node")
    assert py["README.md"].startswith("# Python")
    assert node["README.md"].startswith("# Node")


def test_repo_init_success(monkeypatch):
    client = TestClient(app)

    monkeypatch.setattr(
        "backend.repo_init_agent.requests.post",
        lambda *a, **k: make_resp(data={"html_url": "u/r", "owner": {"login": "u"}}),
    )
    monkeypatch.setattr(
        "backend.repo_init_agent.requests.put",
        lambda *a, **k: make_resp(),
    )
    monkeypatch.setattr(
        "backend.repo_init_agent.store_repo_snapshot",
        lambda *a, **k: "snap123",
    )

    monkeypatch.setenv("GITHUB_TOKEN", "t")

    resp = client.post(
        "/api/repo-init",
        json={
            "project_name": "r",
            "description": "d",
            "language": "python",
            "private": True,
            "ci": "github-actions",
        },
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "success"


def test_repo_init_failure(monkeypatch):
    client = TestClient(app)

    monkeypatch.setattr(
        "backend.repo_init_agent.requests.post",
        lambda *a, **k: make_resp(status=400, data={"msg": "fail"}),
    )
    monkeypatch.setenv("GITHUB_TOKEN", "t")

    resp = client.post(
        "/api/repo-init",
        json={
            "project_name": "r",
            "description": "d",
            "language": "python",
        },
    )
    assert resp.status_code == 400
    assert "fail" in resp.json()["detail"]
