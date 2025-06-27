class EffortEvaluator:
    """Analyze effort based on feedback text."""

    def analyze(self, feedback: str) -> str:
        """Return a simple effort classification."""
        feedback = feedback.lower()
        if "error" in feedback or "failed" in feedback:
            return "high"
        return "low"


class ConfidenceRegulator:
    """Generate strategy updates based on effort analysis."""

    def regulate(self, effort: str) -> str:
        """Return an instruction string."""
        if effort == "high":
            return "increase test coverage and review logic"
        return "continue with current approach"
