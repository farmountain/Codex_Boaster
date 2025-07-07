"""FastAPI application entry point for Codex Booster."""

import os

from fastapi import FastAPI, APIRouter, Depends
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import tempfile

from backend.integrations.hipcortex_bridge import HipCortexBridge
from backend.hipcortex_bridge import router as hipcortex_router
from backend.agents.architect_agent import ArchitectAgent
from backend.agents.builder_agent import BuilderAgent
from backend.agents.tester_agent import TesterAgent
from backend.agents.reflexion_agent import ReflexionAgent
from backend.agents.exporter_agent import ExporterAgent
from backend.agents.monetizer_agent import MonetizerAgent
from backend.monetizer_agent import router as payment_router
from backend.services.workflow import build_test_cycle
from backend.marketplace import router as marketplace_router
from backend.architect_agent import router as project_plan_router
from backend.config_agent import router as config_router
from backend.repo_init_agent import router as repo_init_router
from backend.builder_agent import router as code_builder_router
from backend.tester_agent import router as run_test_router
from backend.test_suite_agent import router as test_suite_router
from backend.deploy_agent import router as deploy_router
from backend.reflexion_agent import router as improvement_router
from backend.doc_agent import router as doc_router
from backend.chat_agent import router as chat_router
from backend.terminal_runner import router as terminal_runner_router
from backend.auth import router as auth_router

app = FastAPI(title="Codex Booster")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers for each agent
architect_router = APIRouter(prefix="/architect", tags=["architect"])
builder_router = APIRouter(prefix="/builder", tags=["builder"])
tester_router = APIRouter(prefix="/tester", tags=["tester"])
reflexion_router = APIRouter(prefix="/reflexion", tags=["reflexion"])
exporter_router = APIRouter(prefix="/exporter", tags=["exporter"])
monetizer_router = APIRouter(prefix="/monetizer", tags=["monetizer"])

hipcortex = HipCortexBridge(base_url=os.getenv("HIPCORTEX_URL", "http://hipcortex"))
architect_agent = ArchitectAgent(hipcortex)
builder_agent = BuilderAgent(hipcortex)
tester_agent = TesterAgent(hipcortex)
reflexion_agent = ReflexionAgent(hipcortex)
exporter_agent = ExporterAgent(hipcortex)
monetizer_agent = MonetizerAgent(hipcortex)


def get_architect_agent() -> ArchitectAgent:
    return architect_agent


def get_builder_agent() -> BuilderAgent:
    return builder_agent


def get_tester_agent() -> TesterAgent:
    return tester_agent


def get_reflexion_agent() -> ReflexionAgent:
    return reflexion_agent


def get_exporter_agent() -> ExporterAgent:
    return exporter_agent


def get_monetizer_agent() -> MonetizerAgent:
    return monetizer_agent


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


@app.post("/plan")
async def plan_root(
    req: PlanRequest, agent: ArchitectAgent = Depends(get_architect_agent)
):
    return agent.plan(req.goal)


@app.post("/build")
async def build_root(
    req: BuildRequest, agent: BuilderAgent = Depends(get_builder_agent)
):
    code = agent.build(req.tests)
    return {"code": code}


@app.post("/test")
async def test_root(
    req: RunTestsRequest, agent: TesterAgent = Depends(get_tester_agent)
):
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        (tmp_path / "generated_module.py").write_text(req.code)
        (tmp_path / "test_generated.py").write_text(req.tests)
        success = agent.run_tests(tmpdir)
    return {"success": success, "output": agent.last_output}


@app.post("/reflect")
async def reflect_root(
    req: ReflexRequest, agent: ReflexionAgent = Depends(get_reflexion_agent)
):
    instructions = agent.reflect(req.feedback)
    return {"instructions": instructions}


@app.post("/export")
async def export_root(
    req: ExportRequest, agent: ExporterAgent = Depends(get_exporter_agent)
):
    archive = agent.export(req.path)
    return {"archive": archive}


@app.get("/export/frontend")
async def export_frontend(agent: ExporterAgent = Depends(get_exporter_agent)):
    """Zip the frontend directory and return it as a download."""
    archive = agent.export("frontend")
    return FileResponse(archive, filename=Path(archive).name)


@architect_router.post("/plan")
async def plan_architecture(
    req: PlanRequest, agent: ArchitectAgent = Depends(get_architect_agent)
):
    """Return an architecture plan for the provided goal."""
    return agent.plan(req.goal)


@builder_router.post("/build")
async def build(req: BuildRequest, agent: BuilderAgent = Depends(get_builder_agent)):
    """Generate code from tests."""
    code = agent.build(req.tests)
    return {"code": code}


@builder_router.post("/build_and_test")
async def build_and_test(
    req: BuildRequest,
    builder: BuilderAgent = Depends(get_builder_agent),
    tester: TesterAgent = Depends(get_tester_agent),
    reflexion: ReflexionAgent = Depends(get_reflexion_agent),
):
    """Generate code from tests and run them."""
    success, code = build_test_cycle(req.tests, builder, tester, reflexion)

    latest_test_results["success"] = success
    if not success:
        latest_improvement["suggestion"] = builder.instructions
    else:
        latest_improvement["suggestion"] = ""
    return {"code": code, "success": success}


@tester_router.post("/run")
async def run_tests(
    req: RunTestsRequest, agent: TesterAgent = Depends(get_tester_agent)
):
    """Run tests against provided code."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        (tmp_path / "generated_module.py").write_text(req.code)
        (tmp_path / "test_generated.py").write_text(req.tests)
        success = agent.run_tests(tmpdir)
    return {"success": success, "output": agent.last_output}


@reflexion_router.post("/reflect")
async def reflect(
    req: ReflexRequest, agent: ReflexionAgent = Depends(get_reflexion_agent)
):
    """Provide reflexion feedback."""
    instructions = agent.reflect(req.feedback)
    return {"instructions": instructions}


@exporter_router.post("/export")
async def export(
    req: ExportRequest, agent: ExporterAgent = Depends(get_exporter_agent)
):
    """Export an artifact and return archive path."""
    archive = agent.export(req.path)
    return {"archive": archive}


@monetizer_router.post("/charge")
async def charge(
    req: ChargeRequest, agent: MonetizerAgent = Depends(get_monetizer_agent)
):
    """Charge the user for usage."""
    agent.charge(req.user_id, req.amount)
    return {"status": "charged"}


@app.get("/test_results")
async def get_test_results():
    """Return the latest test results."""
    return latest_test_results


@app.get("/improvement_suggestion")
async def get_improvement_suggestion():
    """Return the latest improvement suggestion."""
    return latest_improvement




app.include_router(architect_router)
app.include_router(builder_router)
app.include_router(tester_router)
app.include_router(reflexion_router)
app.include_router(exporter_router)
app.include_router(payment_router)
app.include_router(monetizer_router)
app.include_router(marketplace_router)
app.include_router(doc_router)
app.include_router(improvement_router)
app.include_router(chat_router)
app.include_router(project_plan_router)
app.include_router(config_router)
app.include_router(repo_init_router)
app.include_router(code_builder_router)
app.include_router(run_test_router)
app.include_router(test_suite_router)
app.include_router(deploy_router)
app.include_router(hipcortex_router)
app.include_router(terminal_runner_router)
app.include_router(auth_router)
