"""FastAPI application entry point for Codex Booster."""

from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
import tempfile

from backend.integrations.hipcortex_bridge import HipCortexBridge
from backend.agents.architect_agent import ArchitectAgent
from backend.agents.builder_agent import BuilderAgent
from backend.agents.tester_agent import TesterAgent
from backend.agents.reflexion_agent import ReflexionAgent
from backend.services.workflow import build_test_cycle

app = FastAPI(title="Codex Booster")

# TODO: include routers for agents and authentication

hipcortex = HipCortexBridge(base_url="http://hipcortex")
architect_agent = ArchitectAgent(hipcortex)
builder_agent = BuilderAgent(hipcortex)
tester_agent = TesterAgent(hipcortex)
reflexion_agent = ReflexionAgent(hipcortex)

# in-memory store for latest test results
latest_test_results = {"success": None, "output": ""}
latest_improvement = {"suggestion": ""}

class PlanRequest(BaseModel):
    goal: str


class BuildRequest(BaseModel):
    tests: str

@app.get("/")
async def root():
    return {"message": "Codex Booster API"}


@app.post("/plan")
async def plan_architecture(req: PlanRequest):
    """Return an architecture plan for the provided goal."""
    return architect_agent.plan(req.goal)


@app.post("/build_and_test")
async def build_and_test(req: BuildRequest):
    """Generate code from tests and run them."""
    success, code = build_test_cycle(
        req.tests, builder_agent, tester_agent, reflexion_agent
    )

    latest_test_results["success"] = success
    if not success:
        latest_improvement["suggestion"] = builder_agent.instructions
    else:
        latest_improvement["suggestion"] = ""
    return {"code": code, "success": success}


@app.get("/test_results")
async def get_test_results():
    """Return the latest test results."""
    return latest_test_results


@app.get("/improvement_suggestion")
async def get_improvement_suggestion():
    """Return the latest improvement suggestion."""
    return latest_improvement
