import backend.reflexion_agent as ra
from fastapi.testclient import TestClient
from backend.main import app


def test_parse_and_emit_trace_posts(monkeypatch):
    captured = {}

    def fake_emit(step, content, score, session_id):
        captured['step'] = step
        captured['content'] = content
        captured['score'] = score
        captured['session'] = session_id

    monkeypatch.setattr(ra, 'emit_confidence_log', fake_emit)
    log = (
        "Step 1: Attempted run failed.\n"
        "Step 2: Hypothesis - missing import.\n"
        "Step 3: Plan retry with fix."
    )
    ra.parse_and_emit_trace('s1', 'ReflexionAgent', log, confidence=0.8)

    assert captured['session'] == 's1'
    assert 'Plan' in captured['step']
    assert captured['score'] == 0.8
    assert 'Hypothesis' in captured['content']


def test_reflexion_endpoint_emits_trace(monkeypatch):
    called = {}

    def fake_emit(session_id, agent, reasoning_log, confidence=None):
        called['session'] = session_id
        called['agent'] = agent
        called['log'] = reasoning_log
        called['conf'] = confidence
        return 0.5

    monkeypatch.setattr(ra, 'parse_and_emit_trace', fake_emit)
    client = TestClient(app)
    payload = {"test_log": "err", "code_snippet": "x", "context": {}}
    resp = client.post('/reflexion', json=payload)
    assert resp.status_code == 200
    assert called['agent'] == 'ReflexionAgent'
    assert called['session'] == resp.json()['snapshot_id']

