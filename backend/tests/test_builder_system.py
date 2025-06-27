import tempfile
from pathlib import Path

from backend.agents.builder_agent import BuilderAgent
from backend.agents.tester_agent import TesterAgent as TA
from backend.integrations.hipcortex_bridge import HipCortexBridge
from unittest.mock import MagicMock


def test_builder_and_tester_integration_passes(tmp_path: Path):
    tests = """
from generated_module import add

def test_add():
    assert add(2, 3) == 5
"""

    hc = HipCortexBridge(base_url="http://test")
    hc.log_event = MagicMock()

    builder = BuilderAgent(hc)
    code = builder.build(tests)

    # write code and tests to temporary directory
    code_file = tmp_path / "generated_module.py"
    code_file.write_text(code)
    test_file = tmp_path / "test_generated.py"
    test_file.write_text(tests)

    tester = TA(hc)
    success = tester.run_tests(str(tmp_path))

    assert success
    # ensure tester logged events
    hc.log_event.assert_any_call({"agent": "tester", "event": "run_tests", "path": str(tmp_path)})
    hc.log_event.assert_any_call({"agent": "tester", "event": "tests_complete", "success": True})
