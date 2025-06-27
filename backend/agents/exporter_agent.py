"""ExporterAgent handles exporting code artifacts."""

from pathlib import Path
import shutil

from .base import BaseAgent
from backend.integrations.hipcortex_bridge import HipCortexBridge

class ExporterAgent(BaseAgent):
    """Exports code or documentation after successful tests."""

    def __init__(self, hipcortex: HipCortexBridge):
        self.hipcortex = hipcortex

    def export(self, artifact_path: str) -> str:
        """Export the generated artifact as a zip archive.

        Parameters
        ----------
        artifact_path:
            Path to the file or directory to export.

        Returns
        -------
        str
            Path to the created archive or an empty string if the artifact does
            not exist.
        """
        path = Path(artifact_path)
        self.hipcortex.log_event(
            {"agent": "exporter", "event": "export_start", "artifact": artifact_path}
        )

        if not path.exists():
            self.hipcortex.log_event(
                {"agent": "exporter", "event": "missing_artifact", "path": artifact_path}
            )
            return ""

        archive = path.with_suffix(".zip")
        if path.is_dir():
            shutil.make_archive(str(archive.with_suffix("")), "zip", root_dir=str(path))
        else:
            shutil.make_archive(
                str(archive.with_suffix("")),
                "zip",
                root_dir=str(path.parent),
                base_dir=path.name,
            )

        self.hipcortex.log_event(
            {"agent": "exporter", "event": "exported", "artifact": str(archive)}
        )
        return str(archive)
