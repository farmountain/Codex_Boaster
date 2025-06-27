"""BuilderAgent follows TDD principles to generate code."""

from .base import BaseAgent
from backend.integrations.hipcortex_bridge import HipCortexBridge

class BuilderAgent(BaseAgent):
    """Generates code to satisfy tests."""

    def __init__(self, hipcortex: HipCortexBridge):
        self.hipcortex = hipcortex
        self.instructions = ""

    def update_instructions(self, instructions: str) -> None:
        """Update build strategy based on reflexion."""
        self.instructions = instructions
        self.hipcortex.log_event(
            {
                "agent": "builder",
                "event": "update_instructions",
                "instructions": instructions,
            }
        )

    def build(self, tests: str) -> str:
        """Return code that passes the provided tests."""
        # very naive TDD cycle - examine tests and generate minimal code
        self.hipcortex.log_event({"agent": "builder", "event": "start_build", "tests": tests})

        code = "# TODO: generated code"

        if "add(" in tests:
            # simple heuristic to satisfy an add() function test
            code = "def add(a, b):\n    return a + b\n"

        self.hipcortex.log_event({"agent": "builder", "event": "generated_code", "code": code})
        return code
