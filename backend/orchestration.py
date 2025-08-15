"""Utilities for orchestration policies and artifact management."""

from pathlib import Path
from typing import Any


class GuardrailPolicy:
    """Simple guardrail checks for incoming plans or runs."""

    def validate_plan(self, plan: str) -> None:
        """Validate that a plan is safe to execute."""

        if not plan:
            raise ValueError("Plan must not be empty")
        # Extremely small example guardrail to demonstrate policy hooks
        if "DROP TABLE" in plan.upper():
            raise ValueError("Plan contains disallowed content")


class ReviewGate:
    """Placeholder for review approval logic."""

    def approve(self, run: Any) -> bool:
        """Approve a run. In real scenarios this might contact human reviewers."""

        return True


class ArtifactStorage:
    """Store artifacts for runs on the local filesystem."""

    def __init__(self, base_dir: str = "artifacts") -> None:
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save_text(self, run_id: int, name: str, content: str) -> str:
        """Persist a text artifact for a run and return its path."""

        run_dir = self.base_dir / str(run_id)
        run_dir.mkdir(parents=True, exist_ok=True)
        path = run_dir / name
        path.write_text(content)
        return str(path)

