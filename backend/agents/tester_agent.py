"""TesterAgent executes tests and reports results."""

from .base import BaseAgent
from backend.integrations.hipcortex_bridge import HipCortexBridge

class TesterAgent(BaseAgent):
    """Runs tests for generated code."""

    def __init__(self, hipcortex: HipCortexBridge):
        self.hipcortex = hipcortex

    def run_tests(self, code_path: str) -> bool:
        """Execute tests at ``code_path`` and return ``True`` on success."""
        import subprocess
        import sys

        self.hipcortex.log_event({"agent": "tester", "event": "run_tests", "path": code_path})

        proc = subprocess.run(
            [sys.executable, "-m", "pytest", code_path, "-q"],
            capture_output=True,
            text=True,
        )

        success = proc.returncode == 0
        self.hipcortex.log_event(
            {
                "agent": "tester",
                "event": "tests_complete",
                "success": success,
                "output": proc.stdout + proc.stderr,
            }
        )
        return success
