from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict


class PolicyEngine:
    """Simple policy enforcement for tool allow-lists and PII scrubbing."""

    def __init__(self, project_path: Path) -> None:
        policy_file = project_path / "policy.json"
        self.allowed = set()
        self.patterns = []
        if policy_file.exists():
            data = json.loads(policy_file.read_text())
            self.allowed = set(data.get("allowed_tools", []))
            self.patterns = [re.compile(p) for p in data.get("pii_patterns", [])]

    def check_tool(self, name: str) -> bool:
        return not self.allowed or name in self.allowed

    def scrub_pii(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        def scrub(value):
            if isinstance(value, str):
                for pat in self.patterns:
                    value = pat.sub("[REDACTED]", value)
                return value
            if isinstance(value, dict):
                return {k: scrub(v) for k, v in value.items()}
            if isinstance(value, list):
                return [scrub(v) for v in value]
            return value

        return {k: scrub(v) for k, v in payload.items()}


__all__ = ["PolicyEngine"]
