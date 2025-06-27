from backend.agents.builder_agent import BuilderAgent
from backend.integrations.hipcortex_bridge import HipCortexBridge
from unittest.mock import MagicMock


def test_build_returns_code_and_logs():
    hc = HipCortexBridge(base_url="http://test")
    hc.log_event = MagicMock()
    builder = BuilderAgent(hc)
    tests = """
from generated_module import add

def test_add():
    assert add(1, 2) == 3
"""
    code = builder.build(tests)
    assert isinstance(code, str)
    hc.log_event.assert_any_call({"agent": "builder", "event": "start_build", "tests": tests})
    hc.log_event.assert_any_call({"agent": "builder", "event": "generated_code", "code": code})


def test_builder_includes_instructions_comment():
    hc = HipCortexBridge(base_url="http://test")
    hc.log_event = MagicMock()
    builder = BuilderAgent(hc)
    builder.update_instructions("note")
    code = builder.build("from generated_module import foo")
    assert code.startswith("# instructions: note")
