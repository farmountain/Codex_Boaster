"""TesterAgent executes tests and reports results."""

from .base import BaseAgent
from backend.integrations.hipcortex_bridge import HipCortexBridge

class TesterAgent(BaseAgent):
    """Runs tests for generated code."""

    def __init__(self, hipcortex: HipCortexBridge, runner: list[str] | None = None) -> None:
        self.hipcortex = hipcortex
        self.runner = runner
        self.last_output = ""

    def run_tests(self, code_path: str) -> bool:
        """Execute tests at ``code_path`` and return ``True`` on success."""
        import subprocess
        import sys

        cmd = self.runner or [sys.executable, "-m", "pytest", "-q"]
        cmd = cmd + [code_path]

        self.hipcortex.log_event({"agent": "tester", "event": "run_tests", "path": code_path})

        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
        )

        success = proc.returncode == 0
        self.last_output = proc.stdout + proc.stderr
        self.hipcortex.log_event(
            {
                "agent": "tester",
                "event": "tests_complete",
                "success": success,
                "output": self.last_output,
            }
        )
        return success
