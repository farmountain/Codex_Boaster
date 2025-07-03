from backend.reflexion_agent import (
    should_retry,
    reflect_and_retry,
    _retry_counts,
)


def test_should_retry_keywords():
    assert should_retry("contradiction found", 0.4) is True
    assert should_retry("all good", 0.7) is False


def test_reflect_and_retry_respects_limit(monkeypatch):
    calls = []

    def fake_gen(**kwargs):
        calls.append(1)
        return "failed unit test"

    monkeypatch.setattr(
        "backend.reflexion_agent.generate_improvement_suggestions", fake_gen
    )
    monkeypatch.setattr(
        "backend.reflexion_agent.emit_reflexion_log", lambda payload: None
    )
    result = reflect_and_retry("sess", {"test_log": "", "code_snippet": "", "context": {}})
    assert result["attempts"] <= 2
    _retry_counts.clear()
