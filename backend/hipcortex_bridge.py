import os
import json
from datetime import datetime
from hashlib import md5
from urllib import request, error

from backend.integrations.hipcortex_bridge import HipCortexBridge

HIPCORTEX_URL = os.getenv("HIPCORTEX_URL", "http://hipcortex")

bridge = HipCortexBridge(base_url=HIPCORTEX_URL)

def get_current_timestamp() -> str:
    """Return UTC timestamp string."""
    return datetime.utcnow().isoformat()

def log_event(agent: str, payload: dict) -> None:
    """Log an event to HipCortex with agent name."""
    data = {"agent": agent, **payload}
    bridge.log_event(data)

def store_plan_snapshot(prompt: str, modules: list, trace: str) -> str:
    """Persist a plan snapshot and return its id."""
    snapshot = {
        "type": "project_plan",
        "prompt": prompt,
        "modules": modules,
        "trace": trace,
        "timestamp": get_current_timestamp(),
    }
    snapshot_id = md5(json.dumps(snapshot).encode()).hexdigest()
    bridge.log_event({"agent": "architect", "event": "snapshot", "id": snapshot_id, "snapshot": snapshot})
    return snapshot_id

def store_env_snapshot(data: dict) -> str:
    """Persist environment configuration snapshot."""
    snapshot = {
        "type": "env_config",
        "data": data,
        "timestamp": get_current_timestamp(),
    }
    snapshot_id = md5(json.dumps(snapshot).encode()).hexdigest()
    bridge.log_event({"agent": "config", "event": "snapshot", "id": snapshot_id, "snapshot": snapshot})
    return snapshot_id
