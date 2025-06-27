import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient
from backend.main import app


def test_plan_endpoint():
    client = TestClient(app)
    resp = client.post('/architect/plan', json={'goal': 'demo goal'})
    assert resp.status_code == 200
    data = resp.json()
    assert data['goal'] == 'demo goal'
    assert 'modules' in data
