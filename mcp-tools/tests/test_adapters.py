import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from mcp_tools import repo, TOOL_SCHEMAS


def test_repo_adapter_roundtrip():
    result = repo("status", ".")
    assert result["tool"] == "repo"
    assert "repo" in TOOL_SCHEMAS
