import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from goose_runtime import ToolRegistry


def test_list_contains_repo_schema():
    schemas = ToolRegistry.list()
    assert "repo" in schemas
    assert schemas["repo"]["required"] == ["action"]
