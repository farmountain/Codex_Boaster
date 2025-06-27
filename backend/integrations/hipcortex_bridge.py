"""Bridge module to interact with HipCortex memory system."""

# NOTE: All memory operations must go through this module.
# The implementation should call HipCortex APIs without re-implementing logic.

import json
from urllib import request, error


class HipCortexBridge:
    """Simple bridge for HipCortex integration using HTTP calls."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def log_event(self, data: dict) -> None:
        """Send an event to HipCortex for logging.

        Any network errors are silently ignored so the agents keep working even
        when HipCortex is unavailable.
        """

        body = json.dumps(data).encode()
        req = request.Request(
            url=f"{self.base_url}/log",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            request.urlopen(req, timeout=5)
        except error.URLError:
            pass

    def fetch_snapshot(self, snapshot_id: str) -> dict:
        """Retrieve an immutable snapshot from HipCortex."""

        req = request.Request(f"{self.base_url}/snapshot/{snapshot_id}")
        try:
            with request.urlopen(req, timeout=5) as resp:
                return json.load(resp)
        except error.URLError:
            return {}
