"""Registry exposing MCP tool schemas to Goose runtime."""
from __future__ import annotations

from typing import Any, Dict

from mcp_tools.schemas import TOOL_SCHEMAS


class ToolRegistry:
    """Simple in-memory registry backed by shared tool schemas."""

    _schemas: Dict[str, Dict[str, Any]] = TOOL_SCHEMAS

    @classmethod
    def get_schema(cls, name: str) -> Dict[str, Any]:
        return cls._schemas.get(name, {})

    @classmethod
    def list(cls) -> Dict[str, Dict[str, Any]]:
        return cls._schemas


__all__ = ["ToolRegistry"]
