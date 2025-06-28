from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.hipcortex_bridge import log_event, store_plan_snapshot
from backend.reasoning_templates import cot_plan_generator

router = APIRouter()

class PlanInput(BaseModel):
    prompt: str
    context: dict = {}

class PlanOutput(BaseModel):
    modules: list
    reasoning: str
    plan_id: str

@router.post("/architect", response_model=PlanOutput)
async def plan_project(input: PlanInput):
    try:
        plan, trace = cot_plan_generator(input.prompt, context=input.context)
        plan_id = store_plan_snapshot(input.prompt, plan, trace)
        log_event("ArchitectAgent", {"prompt": input.prompt, "plan": plan})
        return PlanOutput(modules=plan, reasoning=trace, plan_id=plan_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
