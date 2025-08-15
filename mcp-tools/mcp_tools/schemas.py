"""Load JSON schemas describing available MCP tools."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any

# shared/tool_schemas.json sits two directories above this file
_SCHEMAS_PATH = Path(__file__).resolve().parents[2] / "shared" / "tool_schemas.json"

with _SCHEMAS_PATH.open("r", encoding="utf-8") as fh:
    TOOL_SCHEMAS: Dict[str, Dict[str, Any]] = json.load(fh)

__all__ = ["TOOL_SCHEMAS"]
