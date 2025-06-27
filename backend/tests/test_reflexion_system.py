from pathlib import Path
from unittest.mock import MagicMock

from backend.integrations.hipcortex_bridge import HipCortexBridge
from backend.agents.builder_agent import BuilderAgent
from backend.agents.tester_agent import TesterAgent
from backend.agents.reflexion_agent import ReflexionAgent
from backend.services.workflow import build_test_cycle


def test_reflexion_invoked_on_failure(tmp_path: Path):
    tests = """\
from generated_module import add

def test_add():
    assert add(1, 2) == 4
"""
    hc = HipCortexBridge(base_url="http://test")
    hc.log_event = MagicMock()

    builder = BuilderAgent(hc)
    tester = TesterAgent(hc)
    reflexion = ReflexionAgent(hc)
    reflexion.reflect = MagicMock(return_value="try again")
    builder.update_instructions = MagicMock()

    success, _ = build_test_cycle(tests, builder, tester, reflexion)

    assert success is False
    reflexion.reflect.assert_called_once()
    builder.update_instructions.assert_called_once_with("try again")

