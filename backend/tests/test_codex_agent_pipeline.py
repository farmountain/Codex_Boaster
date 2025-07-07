import asyncio
from pathlib import Path

import backend.codex_agent as agent_mod
from backend.codex_agent import CodexAgent


def _simple_tests(*args, **kwargs):
    return "from generated_module import add\n\ndef test_add():\n    assert add(1,2)==3\n"


def _simple_code(*args, **kwargs):
    return "def add(a,b):\n    return a + b\n"


async def _dummy_insert(*args, **kwargs):
    return {}


def test_run_pipeline_generates_log(monkeypatch, tmp_path):
    monkeypatch.setattr(agent_mod, "generate_test_cases", _simple_tests)
    monkeypatch.setattr(agent_mod.BuilderAgent, "build", _simple_code)
    monkeypatch.setattr(agent_mod.TesterAgent, "run_tests", lambda self, p: True)
    monkeypatch.setattr(agent_mod.ExporterAgent, "export", lambda self, p: str(Path(p).with_suffix(".zip")))
    monkeypatch.setattr(agent_mod, "SupabaseClient", lambda u, k: type("S", (), {"insert": _dummy_insert})())

    ag = CodexAgent(hipcortex_url="http://test")
    result = asyncio.run(ag.run_pipeline("demo"))

    log_file = Path(result["log_file"])
    assert result["success"] is True
    assert log_file.exists()
    data = log_file.read_text()
    assert "attempt" in data

