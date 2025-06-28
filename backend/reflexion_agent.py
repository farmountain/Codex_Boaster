from fastapi import APIRouter
from pydantic import BaseModel

from .llm_client import generate_improvement_suggestions
from .hipcortex_bridge import (
    log_event,
    store_reflexion_snapshot,
    get_reflexion_logs,
)

router = APIRouter()

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
