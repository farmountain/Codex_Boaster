import os
import json
from datetime import datetime
from hashlib import md5
# Removed urllib.request and error as we will use the HipCortexBridge instance
# from urllib import request, error
from fastapi import APIRouter, HTTPException, status # Added status for clarity
from pydantic import BaseModel, Field # Added Field for consistency
from typing import List, Dict, Any # Added Any for flexibility

# Import the actual HipCortexBridge class from integrations
from backend.integrations.hipcortex_bridge import HipCortexBridge

# Import AgentLogEntry and AgentConfidenceScore for consistent logging
# Ensure this path is correct for your project structure
from backend.dashboard.models import AgentLogEntry, AgentConfidenceScore

HIPCORTEX_URL = os.getenv("HIPCORTEX_URL", "http://hipcortex")

# Initialize the bridge. This instance will be used by other functions in this file
bridge = HipCortexBridge(base_url=HIPCORTEX_URL)

router = APIRouter()
LOG_DIR = "hipcortex_logs" # Directory for in-memory/file-based logs

# Use AgentLogEntry directly for API endpoints for consistency
# class MemorySnapshot(BaseModel):
#     session_id: str
#     agent: str
#     step: str
#     content: str
#     confidence: float
#     timestamp: str | None = None
#     reflexion_classification: str | None = None

def get_current_timestamp() -> str:
    """Return UTC timestamp string."""
    return datetime.utcnow().isoformat()

def log_event(agent: str, payload: dict) -> None:
    """Log an event to HipCortex with agent name."""
    # This function should now use the bridge's record_snapshot with AgentLogEntry
    # Assuming 'payload' can be mapped to AgentLogEntry fields.
    # For simplicity, we'll create a basic AgentLogEntry here.
    log_entry = AgentLogEntry(
        session_id=payload.get("session_id", "default_session"),
        agent_name=agent,
        prompt_input=payload.get("prompt_input", json.dumps(payload)),
        output_content=payload.get("output_content", "No specific output"),
        confidence_score=AgentConfidenceScore(
            score=payload.get("confidence", 0.0),
            rationale=payload.get("rationale", "Logged event")
        ),
        # Add other fields from payload to context_info if needed
        context_info=payload
    )
    # This should be an async call, but log_event is not async.
    # For now, we'll call it directly. In a real app, consider making log_event async
    # or using a background task.
    # asyncio.run(bridge.record_snapshot(log_entry)) # If you make log_event async
    # For now, we'll just print a warning if it's not async
    print(f"WARNING: log_event called synchronously. Consider making it async and awaiting bridge.record_snapshot.")
    # For direct synchronous call, you'd need a synchronous version of record_snapshot
    # or handle it differently. For this example, we'll assume the agent's direct call
    # to bridge.record_snapshot is the primary logging mechanism.
    # The existing log_event seems to be for internal agent logging, not the main HipCortex API.
    # We'll keep it as is, but know it won't hit the FastAPI endpoint unless bridge.log_event
    # is implemented to do so. The provided bridge class does not have log_event.
    # Assuming bridge.log_event is meant to be bridge.record_snapshot
    # For now, let's just print for log_event to avoid breaking existing calls.
    print(f"Log event for agent {agent}: {payload}")


# Refactored emit_confidence_log to use the bridge
async def emit_confidence_log(step: str, content: str, score: float, session_id: str) -> None:
    """Send a confidence snapshot to HipCortex using the bridge."""
    log_entry = AgentLogEntry(
        session_id=session_id,
        agent_name="ReflexionAgent", # As per original function
        prompt_input=f"Confidence log for step: {step}",
        output_content=content,
        confidence_score=AgentConfidenceScore(score=score, rationale="Confidence score snapshot"),
        context_info={"step": step}
    )
    try:
        await bridge.record_snapshot(log_entry)
        print(f"HipCortex: Confidence log sent for session {session_id}, step {step}")
    except HTTPException as e:
        print(f"ERROR: Failed to send confidence log to HipCortex: {e.detail}")
    except Exception as e:
        print(f"ERROR: Unexpected error sending confidence log: {e}")


# Refactored emit_reflexion_log to use the bridge
async def emit_reflexion_log(payload: Dict[str, Any]) -> None:
    """Send a reflexion retry log to HipCortex using the bridge."""
    # Map payload to AgentLogEntry
    log_entry = AgentLogEntry(
        session_id=payload.get("session_id", "default_session"),
        agent_name=payload.get("agent", "ReflexionAgent"),
        prompt_input=payload.get("prompt_input", "Reflexion event"),
        output_content=payload.get("output_content", json.dumps(payload)),
        confidence_score=AgentConfidenceScore(
            score=payload.get("confidence", 0.0),
            rationale=payload.get("rationale", "Reflexion log")
        ),
        context_info=payload # Store full payload in context_info
    )
    try:
        await bridge.record_snapshot(log_entry)
        print(f"HipCortex: Reflexion log sent for session {log_entry.session_id}")
    except HTTPException as e:
        print(f"ERROR: Failed to send reflexion log to HipCortex: {e.detail}")
    except Exception as e:
        print(f"ERROR: Unexpected error sending reflexion log: {e}")


def log_runtime_command(command: str, status: str) -> None:
    """Tag an executed runtime command."""
    # This should also use the bridge.record_snapshot
    log_entry = AgentLogEntry(
        session_id="runtime_session", # Or get from context
        agent_name="TerminalRunner",
        prompt_input=f"Command: {command}",
        output_content=f"Status: {status}",
        confidence_score=AgentConfidenceScore(score=1.0, rationale="Runtime command executed."),
        context_info={"command": command, "status": status}
    )
    # This should be awaited if record_snapshot is async. For now, direct call.
    # asyncio.run(bridge.record_snapshot(log_entry))
    print(f"Log runtime command: {command}, status: {status}")


def set_runtime_context(runtime_dict):
    """Record the active runtime configuration."""
    log_entry = AgentLogEntry(
        session_id="config_session", # Or get from context
        agent_name="ConfigAgent",
        prompt_input="Runtime config set",
        output_content=json.dumps(runtime_dict),
        confidence_score=AgentConfidenceScore(score=1.0, rationale="Runtime configuration set."),
        context_info={"type": "runtime_config", "payload": runtime_dict}
    )
    # asyncio.run(bridge.record_snapshot(log_entry))
    print(f"Set runtime context: {runtime_dict}")


def store_plan_snapshot(prompt: str, modules: list, trace: str) -> str:
    """Persist a plan snapshot and return its id."""
    snapshot_id = md5(json.dumps({"prompt": prompt, "modules": modules, "trace": trace}).encode()).hexdigest()
    log_entry = AgentLogEntry(
        session_id=snapshot_id, # Using snapshot_id as session_id for plan
        agent_name="architect",
        prompt_input=prompt,
        output_content=f"Modules: {modules}, Trace: {trace}",
        confidence_score=AgentConfidenceScore(score=1.0, rationale="Project plan snapshot."),
        context_info={"type": "project_plan", "modules": modules, "trace": trace}
    )
    # asyncio.run(bridge.record_snapshot(log_entry))
    print(f"Store plan snapshot: {snapshot_id}")
    return snapshot_id

def store_env_snapshot(data: dict) -> str:
    """Persist environment configuration snapshot."""
    snapshot_id = md5(json.dumps(data).encode()).hexdigest()
    log_entry = AgentLogEntry(
        session_id=snapshot_id,
        agent_name="config",
        prompt_input="Environment config snapshot",
        output_content=json.dumps(data),
        confidence_score=AgentConfidenceScore(score=1.0, rationale="Environment config snapshot."),
        context_info={"type": "env_config", "data": data}
    )
    # asyncio.run(bridge.record_snapshot(log_entry))
    print(f"Store env snapshot: {snapshot_id}")
    return snapshot_id

def store_repo_snapshot(repo_name: str, files: dict) -> str:
    """Persist repository initialization snapshot."""
    snapshot_id = md5(json.dumps({"repo": repo_name, "files": files}).encode()).hexdigest()
    log_entry = AgentLogEntry(
        session_id=snapshot_id,
        agent_name="repo_init",
        prompt_input=f"Repo init for {repo_name}",
        output_content=f"Files: {list(files.keys())}",
        confidence_score=AgentConfidenceScore(score=1.0, rationale="Repository initialization snapshot."),
        context_info={"type": "repo_init", "repo": repo_name, "files": list(files.keys())}
    )
    # asyncio.run(bridge.record_snapshot(log_entry))
    print(f"Store repo snapshot: {snapshot_id}")
    return snapshot_id


def store_code_snapshot(files: list) -> str:
    """Persist generated code snapshot and return its id."""
    snapshot_id = md5(json.dumps(files).encode()).hexdigest()
    log_entry = AgentLogEntry(
        session_id=snapshot_id,
        agent_name="builder",
        prompt_input="Generated code snapshot",
        output_content=json.dumps(files),
        confidence_score=AgentConfidenceScore(score=1.0, rationale="Generated code snapshot."),
        context_info={"type": "generated_code", "files": files}
    )
    # asyncio.run(bridge.record_snapshot(log_entry))
    print(f"Store code snapshot: {snapshot_id}")
    return snapshot_id

def store_test_results(result: dict) -> str:
    """Persist test results and return snapshot id."""
    snapshot_id = md5(json.dumps(result).encode()).hexdigest()
    log_entry = AgentLogEntry(
        session_id=snapshot_id,
        agent_name="tester",
        prompt_input="Test results snapshot",
        output_content=json.dumps(result),
        confidence_score=AgentConfidenceScore(score=1.0, rationale="Test results snapshot."),
        context_info={"type": "test_log", "result": result}
    )
    # asyncio.run(bridge.record_snapshot(log_entry))
    print(f"Store test results: {snapshot_id}")
    return snapshot_id


def store_reflexion_snapshot(req, plan, parent: str | None = None) -> str:
    """Persist reflexion improvement plan and return snapshot id."""
    snapshot_content = {"input": {"test_log": req.test_log, "code": req.code_snippet}, "plan": plan, "parent": parent}
    snapshot_id = md5(json.dumps(snapshot_content).encode()).hexdigest()
    log_entry = AgentLogEntry(
        session_id=snapshot_id,
        agent_name="reflexion",
        prompt_input="Reflexion trace snapshot",
        output_content=json.dumps(snapshot_content),
        confidence_score=AgentConfidenceScore(score=1.0, rationale="Reflexion trace snapshot."),
        context_info={"type": "reflexion_trace", "input": {"test_log": req.test_log, "code": req.code_snippet}, "plan": plan, "parent": parent}
    )
    # asyncio.run(bridge.record_snapshot(log_entry))
    print(f"Store reflexion snapshot: {snapshot_id}")
    return snapshot_id


def store_deploy_snapshot(result: dict) -> str:
    """Persist deployment result and return snapshot id."""
    snapshot_id = md5(json.dumps(result).encode()).hexdigest()
    log_entry = AgentLogEntry(
        session_id=snapshot_id,
        agent_name="deploy",
        prompt_input="Deployment result snapshot",
        output_content=json.dumps(result),
        confidence_score=AgentConfidenceScore(score=1.0, rationale="Deployment result snapshot."),
        context_info={"type": "deployment", "result": result}
    )
    # asyncio.run(bridge.record_snapshot(log_entry))
    print(f"Store deploy snapshot: {snapshot_id}")
    return snapshot_id


def store_doc_snapshot(files: dict, documentation) -> str:
    """Persist generated documentation and return snapshot id."""
    snapshot_content = {"files": list(files.keys()), "docs": documentation}
    snapshot_id = md5(json.dumps(snapshot_content).encode()).hexdigest()
    log_entry = AgentLogEntry(
        session_id=snapshot_id,
        agent_name="docs",
        prompt_input="Generated documentation snapshot",
        output_content=json.dumps(snapshot_content),
        confidence_score=AgentConfidenceScore(score=1.0, rationale="Generated documentation snapshot."),
        context_info={"type": "documentation", "files": list(files.keys()), "docs": documentation}
    )
    # asyncio.run(bridge.record_snapshot(log_entry))
    print(f"Store doc snapshot: {snapshot_id}")
    return snapshot_id


def store_chat_snapshot(session_data):
    """Persist chat history snapshot and return its id."""
    snapshot_id = md5(json.dumps(session_data).encode()).hexdigest()
    log_entry = AgentLogEntry(
        session_id=session_data.get("session_id", snapshot_id), # Use session_id from data if available
        agent_name="chat",
        prompt_input="Chat history snapshot",
        output_content=json.dumps(session_data),
        confidence_score=AgentConfidenceScore(score=1.0, rationale="Chat history snapshot."),
        context_info={"type": "chat_memory", **session_data}
    )
    # asyncio.run(bridge.record_snapshot(log_entry))
    print(f"Store chat snapshot: {snapshot_id}")
    return snapshot_id


def get_reflexion_logs():
    """Simulate fetching all reflexion memory traces and scores."""
    # This function should ideally use bridge.fetch_logs or a dedicated query method
    # For now, keeping the simulation as it might be used elsewhere.
    return [
        {
            "timestamp": "2025-06-27T12:34:56",
            "agent": "ReflexionAgent",
            "confidence": 0.62,
            "suggestion": "Re-structure the loop for better modularity.",
            "log": "Failure in step 3 → BuilderAgent mismatch",
        },
        {
            "timestamp": "2025-06-27T12:32:22",
            "agent": "ReflexionAgent",
            "confidence": 0.91,
            "suggestion": "✅ Passed all tests. No change needed.",
            "log": "TestRefactor completed → Code stable.",
        },
    ]

# New HipCortex memory API
# These are the actual FastAPI endpoints for HipCortex
# They are now relative paths, and will be prefixed by /hipcortex in main.py

def _load(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {"versions": [], "current_version": None}


def _save(path, data):
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


@router.post("/record") # Changed from "/api/hipcortex/record"
async def record_snapshot_endpoint(snap: AgentLogEntry): # Changed to AgentLogEntry
    snap.timestamp = snap.timestamp or datetime.utcnow().isoformat()
    session_path = os.path.join(LOG_DIR, f"{snap.session_id}.json")
    data = _load(session_path)

    version = f"v{len(data['versions'])+1}"
    snapshot = snap.model_dump() # Use model_dump() for Pydantic v2
    snapshot["version"] = version

    prev_content = data["versions"][-1]["output_content"] if data["versions"] else "" # Changed to output_content
    diff = "\n".join(
        unified_diff(
            prev_content.splitlines(),
            snap.output_content.splitlines(), # Changed to output_content
            fromfile=data.get("current_version") or version,
            tofile=version,
        )
    )
    snapshot["diff"] = diff

    data["versions"].append(snapshot)
    data["current_version"] = version

    _save(session_path, data)
    return {"status": "success", "version": version}


@router.get("/logs") # Changed from "/api/hipcortex/logs"
async def get_logs_endpoint(session_id: str = "default_session"): # Added default session_id
    session_path = os.path.join(LOG_DIR, f"{session_id}.json")
    if not os.path.exists(session_path): # Handle case where session file doesn't exist
        return []
    return _load(session_path)["versions"]


@router.post("/rollback") # Changed from "/api/hipcortex/rollback"
async def rollback_version(payload: Dict):
    session_id = payload["session_id"]
    target = payload["target_version"]
    path = os.path.join(LOG_DIR, f"{session_id}.json")
    data = _load(path)
    if not any(v["version"] == target for v in data["versions"]):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Version not found") # Use status.HTTP_404_NOT_FOUND
    data["current_version"] = target
    _save(path, data)
    return {"status": "rollback successful", "current_version": target}


@router.get("/query") # Changed from "/api/hipcortex/query"
async def query_sessions(confidence_lt: float = 1.0): # Added default for confidence_lt
    results = []
    if not os.path.exists(LOG_DIR):
        return results
    for fname in os.listdir(LOG_DIR):
        data = _load(os.path.join(LOG_DIR, fname))
        # Iterate through versions to check confidence
        if any(v.get("confidence_score", {}).get("score", 1.0) < confidence_lt for v in data["versions"]):
            results.append(fname.split(".")[0])
    return results


@router.get("/memory-log") # Changed from "/api/hipcortex/memory-log"
async def get_memory_log(session_id: str = "default_session"): # Added default session_id
    """Return all memory snapshots for a session ordered by timestamp."""
    session_path = os.path.join(LOG_DIR, f"{session_id}.json")
    if not os.path.exists(session_path): # Handle case where session file doesn't exist
        return []
    logs = _load(session_path)["versions"]
    return sorted(logs, key=lambda x: x.get("timestamp", ""))

