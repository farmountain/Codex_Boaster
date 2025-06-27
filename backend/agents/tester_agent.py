"""TesterAgent executes tests and reports results."""

from .base import BaseAgent
from backend.integrations.hipcortex_bridge import HipCortexBridge

class TesterAgent(BaseAgent):
    """Runs tests for generated code."""

    def __init__(self, hipcortex: HipCortexBridge):
        self.hipcortex = hipcortex

    def run_tests(self, code_path: str) -> bool:
        """Execute tests and return success status."""
        import pytest

        self.hipcortex.log_event({"agent": "tester", "event": "run_tests", "path": code_path})
        # run pytest in quiet mode and return True if exit code is 0
        result = pytest.main([code_path, "-q"])
        success = result == 0
        self.hipcortex.log_event({"agent": "tester", "event": "tests_complete", "success": success})
        return success
