"""ReflexionAgent uses AUREUS framework for self-improvement."""

from .base import BaseAgent
from backend.integrations.hipcortex_bridge import HipCortexBridge
from backend.services.aureus import EffortEvaluator, ConfidenceRegulator

class ReflexionAgent(BaseAgent):
    """Analyzes failed attempts and suggests improvements."""

    def __init__(self, hipcortex: HipCortexBridge):
        self.hipcortex = hipcortex
        self.evaluator = EffortEvaluator()
        self.regulator = ConfidenceRegulator()
        self.last_instructions = ""

    def reflect(self, feedback: str) -> str:
        """Perform reflexion loop and return updated instructions."""
        self.hipcortex.log_event({"agent": "reflexion", "feedback": feedback})

        effort = self.evaluator.analyze(feedback)
        instructions = self.regulator.regulate(effort)

        self.last_instructions = instructions
        self.hipcortex.log_event(
            {
                "agent": "reflexion",
                "effort": effort,
                "instruction": instructions,
            }
        )
        return instructions
