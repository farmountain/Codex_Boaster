from unittest.mock import MagicMock
from backend.integrations.hipcortex_bridge import HipCortexBridge
from backend.agents.builder_agent import BuilderAgent
from backend.agents.tester_agent import TesterAgent
from backend.agents.reflexion_agent import ReflexionAgent
from backend.services.workflow import build_test_cycle


def test_build_test_cycle_success(tmp_path):
    tests = """\
from generated_module import add

def test_add():
    assert add(1, 2) == 3
"""
    hc = HipCortexBridge(base_url="http://test")
    hc.log_event = MagicMock()

    builder = BuilderAgent(hc)
    tester = TesterAgent(hc)
    reflexion = ReflexionAgent(hc)
    reflexion.reflect = MagicMock(return_value="unused")
    builder.update_instructions = MagicMock()

    success, code = build_test_cycle(tests, builder, tester, reflexion)

    assert success is True
    assert "def add" in code
    reflexion.reflect.assert_not_called()
    builder.update_instructions.assert_not_called()
