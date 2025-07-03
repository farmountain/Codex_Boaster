import os
from typing import Any

from .supabase_connector import SupabaseClient

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

_client = None
if SUPABASE_URL and SUPABASE_KEY:
    _client = SupabaseClient(SUPABASE_URL, SUPABASE_KEY)


async def log_event(agent: str, payload: dict[str, Any]):
    """Store an agent event in Supabase."""
    if not _client:
        return
    data = {"agent": agent, **payload}
    try:
        await _client.insert("agent_events", data)
    except Exception as exc:  # pragma: no cover - logging failure shouldn't crash
        print(f"[logger] failed to log event: {exc}")


async def log_snapshot(payload: dict[str, Any]):
    """Store a snapshot payload."""
    if not _client:
        return
    try:
        await _client.insert("snapshots", payload)
    except Exception as exc:  # pragma: no cover
        print(f"[logger] failed to log snapshot: {exc}")
