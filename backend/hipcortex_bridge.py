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

def store_repo_snapshot(repo_name: str, files: dict) -> str:
    """Persist repository initialization snapshot."""
    snapshot = {
        "type": "repo_init",
        "repo": repo_name,
        "files": list(files.keys()),
        "timestamp": get_current_timestamp(),
    }
    snapshot_id = md5(json.dumps(snapshot).encode()).hexdigest()
    bridge.log_event({"agent": "repo_init", "event": "snapshot", "id": snapshot_id, "snapshot": snapshot})
    return snapshot_id


def store_code_snapshot(files: list) -> str:
    """Persist generated code snapshot and return its id."""
    snapshot = {
        "type": "generated_code",
        "files": files,
        "timestamp": get_current_timestamp(),
    }
    snapshot_id = md5(json.dumps(snapshot).encode()).hexdigest()
    bridge.log_event({"agent": "builder", "event": "snapshot", "id": snapshot_id, "snapshot": snapshot})
    return snapshot_id

def store_test_results(result: dict) -> str:
    """Persist test results and return snapshot id."""
    snapshot = {
        "type": "test_log",
        "result": result,
        "timestamp": get_current_timestamp(),
    }
    snapshot_id = md5(json.dumps(snapshot).encode()).hexdigest()
    bridge.log_event({"agent": "tester", "event": "snapshot", "id": snapshot_id, "snapshot": snapshot})
    return snapshot_id


def store_reflexion_snapshot(req, plan) -> str:
    """Persist reflexion improvement plan and return snapshot id."""
    snapshot = {
        "type": "reflexion_trace",
        "input": {"test_log": req.test_log, "code": req.code_snippet},
        "plan": plan,
        "timestamp": get_current_timestamp(),
    }
    snapshot_id = md5(json.dumps(snapshot).encode()).hexdigest()
    bridge.log_event({"agent": "reflexion", "event": "snapshot", "id": snapshot_id, "snapshot": snapshot})
    return snapshot_id


def store_deploy_snapshot(result: dict) -> str:
    """Persist deployment result and return snapshot id."""
    snapshot = {
        "type": "deployment",
        "result": result,
        "timestamp": get_current_timestamp(),
    }
    snapshot_id = md5(json.dumps(snapshot).encode()).hexdigest()
    bridge.log_event({"agent": "deploy", "event": "snapshot", "id": snapshot_id, "snapshot": snapshot})
    return snapshot_id


def store_doc_snapshot(files: dict, documentation) -> str:
    """Persist generated documentation and return snapshot id."""
    snapshot = {
        "type": "documentation",
        "files": list(files.keys()),
        "docs": documentation,
        "timestamp": get_current_timestamp(),
    }
    snapshot_id = md5(json.dumps(snapshot).encode()).hexdigest()
    bridge.log_event({"agent": "docs", "event": "snapshot", "id": snapshot_id, "snapshot": snapshot})
    return snapshot_id
