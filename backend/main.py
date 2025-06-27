"""FastAPI application entry point for Codex Booster."""

from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
import tempfile

from backend.integrations.hipcortex_bridge import HipCortexBridge
from backend.agents.architect_agent import ArchitectAgent
from backend.agents.builder_agent import BuilderAgent
from backend.agents.tester_agent import TesterAgent

app = FastAPI(title="Codex Booster")

# TODO: include routers for agents and authentication

hipcortex = HipCortexBridge(base_url="http://hipcortex")
architect_agent = ArchitectAgent(hipcortex)
builder_agent = BuilderAgent(hipcortex)
tester_agent = TesterAgent(hipcortex)

# in-memory store for latest test results
latest_test_results = {"success": None, "output": ""}

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
    code = builder_agent.build(req.tests)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        (tmp_path / "generated_module.py").write_text(code)
        (tmp_path / "test_generated.py").write_text(req.tests)
        success = tester_agent.run_tests(tmpdir)

    latest_test_results["success"] = success
    return {"code": code, "success": success}


@app.get("/test_results")
async def get_test_results():
    """Return the latest test results."""
    return latest_test_results
