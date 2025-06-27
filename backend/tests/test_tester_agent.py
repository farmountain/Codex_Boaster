from pathlib import Path
from unittest.mock import MagicMock, ANY
import sys

from backend.agents.tester_agent import TesterAgent
from backend.integrations.hipcortex_bridge import HipCortexBridge


def _write_files(dir: Path, code: str, test: str) -> None:
    (dir / "generated.py").write_text(code)
    (dir / "test_generated.py").write_text(test)


def test_run_tests_pass_and_fail(tmp_path: Path):
    passing = tmp_path / "pass"
    failing = tmp_path / "fail"
    passing.mkdir()
    failing.mkdir()

    code = "def add(a, b):\n    return a + b\n"
    passing_test = "from generated import add\n\n\ndef test_add():\n    assert add(1,2) == 3\n"
    failing_test = "from generated import add\n\n\ndef test_add():\n    assert add(1,2) == 4\n"

    _write_files(passing, code, passing_test)
    _write_files(failing, code, failing_test)

    hc = HipCortexBridge(base_url="http://test")
    hc.log_event = MagicMock()
    tester = TesterAgent(hc)

    success = tester.run_tests(str(passing))
    assert success
    hc.log_event.assert_any_call({"agent": "tester", "event": "run_tests", "path": str(passing)})
    hc.log_event.assert_any_call({"agent": "tester", "event": "tests_complete", "success": True, "output": ANY})

    hc.log_event.reset_mock()

    success = tester.run_tests(str(failing))
    assert success is False
    hc.log_event.assert_any_call({"agent": "tester", "event": "run_tests", "path": str(failing)})
    hc.log_event.assert_any_call({"agent": "tester", "event": "tests_complete", "success": False, "output": ANY})


def test_custom_runner(tmp_path: Path):
    runner_script = tmp_path / "runner.py"
    runner_script.write_text(
        "import sys\nprint('custom', sys.argv[1])"
    )

    hc = HipCortexBridge(base_url="http://test")
    hc.log_event = MagicMock()
    tester = TesterAgent(hc, runner=[sys.executable, str(runner_script)])

    success = tester.run_tests("/some/path")
    assert success
    assert "custom /some/path" in tester.last_output
    hc.log_event.assert_any_call({"agent": "tester", "event": "run_tests", "path": "/some/path"})
    hc.log_event.assert_any_call({"agent": "tester", "event": "tests_complete", "success": True, "output": ANY})
