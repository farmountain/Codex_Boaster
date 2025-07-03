from fastapi import APIRouter
from pydantic import BaseModel
import requests
from datetime import datetime

from .llm_client import generate_improvement_suggestions
from .hipcortex_bridge import (
    log_event,
    store_reflexion_snapshot,
    get_reflexion_logs,
    emit_confidence_log,
    emit_reflexion_log,
)
from .services.aureus import compute_confidence

router = APIRouter()

MAX_RETRIES = 2
_retry_counts: dict[str, int] = {}


def should_retry(reasoning: str, confidence: float) -> bool:
    """Return True if reasoning text and confidence warrant another try."""
    if confidence >= 0.6:
        return False
    keywords = [
        "contradiction",
        "failed",
        "ambiguous",
        "retry",
        "unclear",
    ]
    return any(k in reasoning.lower() for k in keywords)


def extract_justification(reasoning: str) -> str:
    """Extract a short justification snippet from reasoning."""
    lines = [l.strip() for l in reasoning.splitlines() if l.strip()]
    for l in lines:
        low = l.lower()
        if any(k in low for k in ["failed", "contradiction", "ambiguous", "hallucination"]):
            return l
    return lines[0] if lines else ""


def update_trace_with_retry(trace: dict, reasoning: str) -> dict:
    """Return a new trace including retry reasoning."""
    new_trace = dict(trace)
    new_trace.setdefault("retries", []).append(reasoning)
    return new_trace


def reflect_and_retry(session_id: str, input_trace: dict) -> dict:
    """Generate reasoning and retry instructions with logging."""
    retries = _retry_counts.get(session_id, 0)
    trace = input_trace
    while retries < MAX_RETRIES:
        reasoning = generate_improvement_suggestions(**trace)
        confidence = compute_confidence(reasoning if isinstance(reasoning, str) else str(reasoning))
        justification = extract_justification(reasoning if isinstance(reasoning, str) else str(reasoning))
        log_reflexion = {
            "type": "retry" if retries > 0 else "initial",
            "attempt": retries,
            "reasoning": reasoning,
            "confidence": confidence,
            "justification": justification,
        }
        emit_reflexion_log(log_reflexion)
        if not should_retry(reasoning if isinstance(reasoning, str) else str(reasoning), confidence):
            break
        retries += 1
        _retry_counts[session_id] = retries
        trace = update_trace_with_retry(trace, reasoning)
    return {"plan": reasoning, "attempts": retries}


def parse_and_emit_trace(
    session_id: str,
    agent: str,
    reasoning_log: str,
    confidence: float | None = None,
) -> float:
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

    score = confidence if confidence is not None else compute_confidence(reasoning_log)
    payload_content = "\n".join(filter(None, [cause, hypothesis, action]))
    try:
        emit_confidence_log(action or "Reflexion Step", payload_content, score, session_id)
    except Exception as e:  # pragma: no cover - network failure shouldn't crash
        print(f"[HipCortex] Failed to log reasoning trace: {e}")
    return score

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
