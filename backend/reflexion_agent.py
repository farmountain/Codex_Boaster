from fastapi import APIRouter
from pydantic import BaseModel
import requests
from datetime import datetime

from .llm_client import generate_improvement_suggestions
from .hipcortex_bridge import (
    log_event,
    store_reflexion_snapshot,
    get_reflexion_logs,
)

router = APIRouter()


def parse_and_emit_trace(
    session_id: str,
    agent: str,
    reasoning_log: str,
    confidence: float = 0.7,
) -> None:
    """Parse a free-form reasoning log and persist it via HipCortex."""
    steps = [s.strip() for s in reasoning_log.strip().split("\n") if s.strip()]
    cause = ""
    hypothesis = ""
    action = ""
    for line in steps:
        low = line.lower()
        if "attempt" in low or "error" in low:
            cause = line
        elif "hypothesis" in low:
            hypothesis = line
        elif "plan" in low or "retry" in low:
            action = line

    payload = {
        "session_id": session_id,
        "agent": agent,
        "step": action or "Reflexion Step",
        "content": "\n".join(filter(None, [cause, hypothesis, action])),
        "confidence": confidence,
        "timestamp": datetime.utcnow().isoformat(),
    }
    try:
        requests.post("http://localhost:8000/api/hipcortex/record", json=payload)
    except Exception as e:  # pragma: no cover - network failure shouldn't crash
        print(f"[HipCortex] Failed to log reasoning trace: {e}")

class ReflexionRequest(BaseModel):
    test_log: str
    code_snippet: str
    context: dict = {}

@router.post("/reflexion")
async def reflect(req: ReflexionRequest):
    plan = generate_improvement_suggestions(
        test_log=req.test_log,
        code=req.code_snippet,
        context=req.context
    )
    snapshot_id = store_reflexion_snapshot(req, plan)
    parse_and_emit_trace(
        snapshot_id,
        "ReflexionAgent",
        plan if isinstance(plan, str) else str(plan),
        confidence=plan.get("confidence", 0.7) if isinstance(plan, dict) else 0.7,
    )
    log_event("ReflexionAgent", {
        "test_summary": req.test_log[:200],
        "steps": len(plan.get("steps", [])) if isinstance(plan, dict) else 0,
        "confidence": plan.get("confidence", "N/A") if isinstance(plan, dict) else "N/A"
    })
    return {"plan": plan, "snapshot_id": snapshot_id}


@router.get("/reflexion/logs")
def fetch_reflexion_logs():
    logs = get_reflexion_logs()
    return logs
