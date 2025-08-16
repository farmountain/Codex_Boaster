"""Simple local hub to spawn tool servers and forward remote calls."""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

from .tool import call_tool
from .policy import PolicyEngine


class LocalHub:
    """Manage tool servers locally or forward to a remote Boaster instance."""

    def __init__(self, boaster_url: Optional[str] = None, project_path: Optional[str] = None) -> None:
        self.boaster_url = boaster_url
        self._procs: Dict[str, subprocess.Popen] = {}
        self._policy = (
            PolicyEngine(Path(project_path)) if project_path else None
        )

    def spawn(self, name: str, cmd: List[str]) -> None:
        """Spawn a tool server if not already running."""
        proc = self._procs.get(name)
        if proc and proc.poll() is None:
            return
        self._procs[name] = subprocess.Popen(cmd)

    def call(self, tool: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke a tool locally or remotely."""
        if self._policy and not self._policy.check_tool(tool):
            raise PermissionError(f"Tool {tool} not allowed")
        if self._policy:
            payload = self._policy.scrub_pii(payload)
        if self.boaster_url:
            response = requests.post(
                f"{self.boaster_url}/tools/{tool}", json=payload, timeout=30
            )
            response.raise_for_status()
            return response.json()
        return call_tool(tool, payload)

    def shutdown(self) -> None:
        """Terminate all spawned processes."""
        for proc in self._procs.values():
            try:
                proc.terminate()
            except Exception:
                pass
        self._procs.clear()


__all__ = ["LocalHub"]
