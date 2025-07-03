import json
from pathlib import Path


WEIGHT_FILE = Path(__file__).with_name("aureus_weights.json")


def load_weights() -> dict:
    """Load scoring weights from aureus_weights.json."""
    if WEIGHT_FILE.exists():
        with open(WEIGHT_FILE) as f:
            return json.load(f)
    return {"base": 0.5, "evidence": 0.1, "retry": -0.2, "success": 0.2, "contradiction": -0.3}


def compute_confidence(reasoning_log: str, weights: dict | None = None) -> float:
    """Compute a confidence score using symbolic heuristics."""
    weights = weights or load_weights()
    score = weights.get("base", 0.5)
    low = reasoning_log.lower()
    if "retry" in low:
        score += weights.get("retry", -0.2)
    if "based on" in low or "found in trace" in low:
        score += weights.get("evidence", 0.1)
    if "success" in low or "test passed" in low:
        score += weights.get("success", 0.2)
    if "contradiction" in low or "conflict" in low:
        score += weights.get("contradiction", -0.3)
    return max(0.0, min(1.0, score))


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
