import json
from pathlib import Path

import pytest

from mcp_tools import LocalHub


def test_policy_allowlist_and_scrub(tmp_path: Path):
    policy = {
        "allowed_tools": ["echo"],
        "pii_patterns": ["secret"],
    }
    (tmp_path / "policy.json").write_text(json.dumps(policy))
    hub = LocalHub(project_path=str(tmp_path))

    assert hub.call("echo", {"msg": "ok"})["tool"] == "echo"

    with pytest.raises(PermissionError):
        hub.call("other", {})

    result = hub.call("echo", {"msg": "contains secret"})
    assert result["payload"]["msg"] == "contains [REDACTED]"
