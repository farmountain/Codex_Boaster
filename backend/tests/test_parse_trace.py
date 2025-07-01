import backend.reflexion_agent as ra
from fastapi.testclient import TestClient
from backend.main import app


def test_parse_and_emit_trace_posts(monkeypatch):
    captured = {}

    def fake_post(url, json):
        captured['url'] = url
        captured['payload'] = json
        class R:
            status_code = 200
        return R()

    monkeypatch.setattr(ra.requests, 'post', fake_post)
    log = (
        "Step 1: Attempted run failed.\n"
        "Step 2: Hypothesis - missing import.\n"
        "Step 3: Plan retry with fix."
    )
    ra.parse_and_emit_trace('s1', 'ReflexionAgent', log, confidence=0.8)

    assert captured['url'] == 'http://localhost:8000/api/hipcortex/record'
    assert captured['payload']['session_id'] == 's1'
    assert captured['payload']['agent'] == 'ReflexionAgent'
    assert 'Hypothesis' in captured['payload']['content']


def test_reflexion_endpoint_emits_trace(monkeypatch):
    called = {}

    def fake_emit(session_id, agent, reasoning_log, confidence=0.7):
        called['session'] = session_id
        called['agent'] = agent
        called['log'] = reasoning_log
        called['conf'] = confidence

    monkeypatch.setattr(ra, 'parse_and_emit_trace', fake_emit)
    client = TestClient(app)
    payload = {"test_log": "err", "code_snippet": "x", "context": {}}
    resp = client.post('/reflexion', json=payload)
    assert resp.status_code == 200
    assert called['agent'] == 'ReflexionAgent'
    assert called['session'] == resp.json()['snapshot_id']

