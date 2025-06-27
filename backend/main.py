"""FastAPI application entry point for Codex Booster."""

from fastapi import FastAPI
from pydantic import BaseModel

from backend.integrations.hipcortex_bridge import HipCortexBridge
from backend.agents.architect_agent import ArchitectAgent

app = FastAPI(title="Codex Booster")

# TODO: include routers for agents and authentication

hipcortex = HipCortexBridge(base_url="http://hipcortex")
architect_agent = ArchitectAgent(hipcortex)

class PlanRequest(BaseModel):
    goal: str

@app.get("/")
async def root():
    return {"message": "Codex Booster API"}


@app.post("/plan")
async def plan_architecture(req: PlanRequest):
    """Return an architecture plan for the provided goal."""
    return architect_agent.plan(req.goal)
