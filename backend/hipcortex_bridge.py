import os
import json
from datetime import datetime
from hashlib import md5
from urllib import request, error
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from difflib import unified_diff

from backend.integrations.hipcortex_bridge import HipCortexBridge

HIPCORTEX_URL = os.getenv("HIPCORTEX_URL", "http://hipcortex")

bridge = HipCortexBridge(base_url=HIPCORTEX_URL)

router = APIRouter()
LOG_DIR = "hipcortex_logs"
class MemorySnapshot(BaseModel):
    session_id: str
    agent: str
    step: str
    content: str
    confidence: float
    timestamp: str | None = None
    reflexion_classification: str | None = None


def get_current_timestamp() -> str:
    """Return UTC timestamp string."""
    return datetime.utcnow().isoformat()

def log_event(agent: str, payload: dict) -> None:
    """Log an event to HipCortex with agent name."""
    data = {"agent": agent, **payload}
    bridge.log_event(data)


def emit_confidence_log(step: str, content: str, score: float, session_id: str) -> None:
    """Send a confidence snapshot to HipCortex."""
    payload = {
        "agent": "ReflexionAgent",
        "step": step,
        "content": content,
        "confidence": score,
        "timestamp": get_current_timestamp(),
        "session_id": session_id,
    }
    try:
        request.urlopen(
            request.Request(
                url=f"{HIPCORTEX_URL}/api/hipcortex/record",
                data=json.dumps(payload).encode(),
                headers={"Content-Type": "application/json"},
                method="POST",
            ),
            timeout=5,
        )
    except error.URLError:
        pass


def log_runtime_command(command: str, status: str) -> None:
    """Tag an executed runtime command."""
    log_event("TerminalRunner", {"command": command, "status": status})


def set_runtime_context(runtime_dict):
    """Record the active runtime configuration."""
    log_event(
        "ConfigAgent",
        {
            "type": "runtime_config",
            "payload": runtime_dict,
        },
    )

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


def store_chat_snapshot(session_data):
    """Persist chat history snapshot and return its id."""
    snapshot = {
        "type": "chat_memory",
        **session_data,
        "timestamp": get_current_timestamp(),
    }
    snapshot_id = md5(json.dumps(snapshot).encode()).hexdigest()
    bridge.log_event({"agent": "chat", "event": "snapshot", "id": snapshot_id, "snapshot": snapshot})
    return snapshot_id


def get_reflexion_logs():
    """Simulate fetching all reflexion memory traces and scores."""
    return [
        {
            "timestamp": "2025-06-27T12:34:56",
            "agent": "ReflexionAgent",
            "confidence": 0.62,
            "suggestion": "Re-structure the loop for better modularity.",
            "log": "Failure in step 3 \u2192 BuilderAgent mismatch",
        },
        {
            "timestamp": "2025-06-27T12:32:22",
            "agent": "ReflexionAgent",
            "confidence": 0.91,
            "suggestion": "\u2705 Passed all tests. No change needed.",
            "log": "TestRefactor completed \u2192 Code stable.",
        },
    ]

# New HipCortex memory API



def _load(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {"versions": [], "current_version": None}


def _save(path, data):
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


@router.post("/api/hipcortex/record")
async def record_snapshot(snap: MemorySnapshot):
    snap.timestamp = snap.timestamp or datetime.utcnow().isoformat()
    session_path = os.path.join(LOG_DIR, f"{snap.session_id}.json")
    data = _load(session_path)

    version = f"v{len(data['versions'])+1}"
    snapshot = snap.dict()
    snapshot["version"] = version

    prev_content = data["versions"][-1]["content"] if data["versions"] else ""
    diff = "\n".join(
        unified_diff(
            prev_content.splitlines(),
            snap.content.splitlines(),
            fromfile=data.get("current_version") or version,
            tofile=version,
        )
    )
    snapshot["diff"] = diff

    data["versions"].append(snapshot)
    data["current_version"] = version

    _save(session_path, data)
    return {"status": "success", "version": version}


@router.get("/api/hipcortex/logs")
async def get_logs(session_id: str):
    session_path = os.path.join(LOG_DIR, f"{session_id}.json")
    return _load(session_path)["versions"]


@router.post("/api/hipcortex/rollback")
async def rollback_version(payload: Dict):
    session_id = payload["session_id"]
    target = payload["target_version"]
    path = os.path.join(LOG_DIR, f"{session_id}.json")
    data = _load(path)
    if not any(v["version"] == target for v in data["versions"]):
        raise HTTPException(status_code=404, detail="Version not found")
    data["current_version"] = target
    _save(path, data)
    return {"status": "rollback successful", "current_version": target}


@router.get("/api/hipcortex/query")
async def query_sessions(confidence_lt: float):
    results = []
    if not os.path.exists(LOG_DIR):
        return results
    for fname in os.listdir(LOG_DIR):
        data = _load(os.path.join(LOG_DIR, fname))
        if any(v.get("confidence", 1.0) < confidence_lt for v in data["versions"]):
            results.append(fname.split(".")[0])
    return results

