from pathlib import Path
from unittest.mock import MagicMock

from backend.agents.exporter_agent import ExporterAgent
from backend.integrations.hipcortex_bridge import HipCortexBridge


def test_export_creates_archive_and_logs(tmp_path: Path):
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    (src_dir / "file.txt").write_text("content")

    hc = HipCortexBridge(base_url="http://test")
    hc.log_event = MagicMock()
    agent = ExporterAgent(hc)

    archive = agent.export(str(src_dir))
    assert archive.endswith(".zip")
    assert Path(archive).exists()
    hc.log_event.assert_any_call({"agent": "exporter", "event": "export_start", "artifact": str(src_dir)})
    hc.log_event.assert_any_call({"agent": "exporter", "event": "exported", "artifact": archive})


def test_export_handles_missing_path(tmp_path: Path):
    missing = tmp_path / "missing"
    hc = HipCortexBridge(base_url="http://test")
    hc.log_event = MagicMock()
    agent = ExporterAgent(hc)

    archive = agent.export(str(missing))
    assert archive == ""
    hc.log_event.assert_any_call({"agent": "exporter", "event": "missing_artifact", "path": str(missing)})
