"""ExporterAgent handles exporting code artifacts."""

from .base import BaseAgent
from backend.integrations.hipcortex_bridge import HipCortexBridge

class ExporterAgent(BaseAgent):
    """Exports code or documentation after successful tests."""

    def __init__(self, hipcortex: HipCortexBridge):
        self.hipcortex = hipcortex

    def export(self, artifact_path: str) -> None:
        """Export the generated artifact."""
        self.hipcortex.log_event({"agent": "exporter", "artifact": artifact_path})
        # TODO: implement export logic
