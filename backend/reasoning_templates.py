"""Simple reasoning template helpers for planning."""

from typing import Tuple, List, Dict


def cot_plan_generator(prompt: str, context: dict | None = None) -> Tuple[List[Dict[str, str]], str]:
    """Return a fake chain-of-thought plan and reasoning trace."""
    reasoning = f"Plan generated for: {prompt}"
    modules = [
        {"name": "frontend", "description": "User interface"},
        {"name": "backend", "description": "API server"},
    ]
    return modules, reasoning
