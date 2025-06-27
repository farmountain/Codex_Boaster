"""FastAPI application entry point for Codex Booster."""

from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from pathlib import Path
import tempfile

from backend.integrations.hipcortex_bridge import HipCortexBridge
from backend.agents.architect_agent import ArchitectAgent
from backend.agents.builder_agent import BuilderAgent
from backend.agents.tester_agent import TesterAgent
from backend.agents.reflexion_agent import ReflexionAgent
from backend.agents.exporter_agent import ExporterAgent
from backend.agents.monetizer_agent import MonetizerAgent
from backend.services.workflow import build_test_cycle

app = FastAPI(title="Codex Booster")

# Routers for each agent
architect_router = APIRouter(prefix="/architect", tags=["architect"])
builder_router = APIRouter(prefix="/builder", tags=["builder"])
tester_router = APIRouter(prefix="/tester", tags=["tester"])
reflexion_router = APIRouter(prefix="/reflexion", tags=["reflexion"])
exporter_router = APIRouter(prefix="/exporter", tags=["exporter"])
monetizer_router = APIRouter(prefix="/monetizer", tags=["monetizer"])

app.include_router(architect_router)
app.include_router(builder_router)
app.include_router(tester_router)
app.include_router(reflexion_router)
app.include_router(exporter_router)
app.include_router(monetizer_router)

hipcortex = HipCortexBridge(base_url="http://hipcortex")
architect_agent = ArchitectAgent(hipcortex)
builder_agent = BuilderAgent(hipcortex)
tester_agent = TesterAgent(hipcortex)
reflexion_agent = ReflexionAgent(hipcortex)
exporter_agent = ExporterAgent(hipcortex)
monetizer_agent = MonetizerAgent(hipcortex, api_key="sk_test")

# in-memory store for latest test results
latest_test_results = {"success": None, "output": ""}
latest_improvement = {"suggestion": ""}

class PlanRequest(BaseModel):
    goal: str


class BuildRequest(BaseModel):
    tests: str


class RunTestsRequest(BaseModel):
    code: str
    tests: str


class ReflexRequest(BaseModel):
    feedback: str


class ExportRequest(BaseModel):
    path: str


class ChargeRequest(BaseModel):
    user_id: str
    amount: int

@app.get("/")
async def root():
    return {"message": "Codex Booster API"}


@architect_router.post("/plan")
async def plan_architecture(req: PlanRequest):
    """Return an architecture plan for the provided goal."""
    return architect_agent.plan(req.goal)


@builder_router.post("/build")
async def build(req: BuildRequest):
    """Generate code from tests."""
    code = builder_agent.build(req.tests)
    return {"code": code}


@builder_router.post("/build_and_test")
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


@tester_router.post("/run")
async def run_tests(req: RunTestsRequest):
    """Run tests against provided code."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        (tmp_path / "generated_module.py").write_text(req.code)
        (tmp_path / "test_generated.py").write_text(req.tests)
        success = tester_agent.run_tests(tmpdir)
    return {"success": success, "output": tester_agent.last_output}


@reflexion_router.post("/reflect")
async def reflect(req: ReflexRequest):
    """Provide reflexion feedback."""
    instructions = reflexion_agent.reflect(req.feedback)
    return {"instructions": instructions}


@exporter_router.post("/export")
async def export(req: ExportRequest):
    """Export an artifact and return archive path."""
    archive = exporter_agent.export(req.path)
    return {"archive": archive}


@monetizer_router.post("/charge")
async def charge(req: ChargeRequest):
    """Charge the user for usage."""
    monetizer_agent.charge(req.user_id, req.amount)
    return {"status": "charged"}


@app.get("/test_results")
async def get_test_results():
    """Return the latest test results."""
    return latest_test_results


@app.get("/improvement_suggestion")
async def get_improvement_suggestion():
    """Return the latest improvement suggestion."""
    return latest_improvement
