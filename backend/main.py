from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from backend.auth import delete_account
# ...existing code...
# ...existing code...

# backend/main.py (relevant section for imports and router inclusion)
# ...existing code...
app = FastAPI(title="Codex Booster")
# ...existing code...

    # /auth/delete_account endpoint is now registered via auth_router
# backend/main.py (relevant section for imports and router inclusion)

import os

from fastapi import FastAPI, APIRouter, Depends
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import tempfile
from backend.telemetry import setup_telemetry

# Import HipCortexBridge and its router
from backend.integrations.hipcortex_bridge import HipCortexBridge
from backend.hipcortex_bridge import router as hipcortex_router

# Import your agents
from backend.agents.architect_agent import ArchitectAgent
from backend.agents.builder_agent import BuilderAgent
from backend.agents.tester_agent import TesterAgent
from backend.agents.reflexion_agent import ReflexionAgent
from backend.agents.exporter_agent import ExporterAgent
from backend.agents.monetizer_agent import MonetizerAgent

# Import other routers you have defined
from backend.monetizer_agent import router as payment_router
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

# Import workflow service (if needed for direct calls, though agents might wrap it)
from backend.services.workflow import build_test_cycle

# Import your new MCP router's creation function
from backend.mcp_router import create_mcp_router

app = FastAPI(title="Codex Booster")

# Configure CORS for local development and Copilot access
# IMPORTANT: In production, restrict origins!
origins = [
    "http://localhost:3000",  # Your frontend
    "http://127.0.0.1:3000",
    "vscode-webview://*", # This might be needed for VS Code webview context
    "https://*.ngrok-free.app", # If using ngrok
    "https://*.github.dev" # For github.dev codespaces or web IDE
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if os.getenv("ENABLE_OTEL", "1") == "1":
    setup_telemetry("codex-booster")

# --- Define APIRouter instances here, BEFORE they are used ---
architect_router = APIRouter(prefix="/architect", tags=["architect"])
builder_router = APIRouter(prefix="/builder", tags=["builder"])
tester_router = APIRouter(prefix="/tester", tags=["tester"])
reflexion_router = APIRouter(prefix="/reflexion", tags=["reflexion"])
exporter_router = APIRouter(prefix="/exporter", tags=["exporter"])
monetizer_router = APIRouter(prefix="/monetizer", tags=["monetizer"])
# --- End APIRouter definitions ---
architect_router = APIRouter(prefix="/architect", tags=["architect"])
builder_router = APIRouter(prefix="/builder", tags=["builder"])
tester_router = APIRouter(prefix="/tester", tags=["tester"])
reflexion_router = APIRouter(prefix="/reflexion", tags=["reflexion"])
exporter_router = APIRouter(prefix="/exporter", tags=["exporter"])
monetizer_router = APIRouter(prefix="/monetizer", tags=["monetizer"])
# --- End APIRouter definitions ---


# Initialize HipCortexBridge
hipcortex = HipCortexBridge(base_url=os.getenv("HIPCORTEX_URL", "http://hipcortex"))

# Initialize your agents with the HipCortexBridge instance
architect_agent = ArchitectAgent(hipcortex)
builder_agent = BuilderAgent(hipcortex)
tester_agent = TesterAgent(hipcortex)
reflexion_agent = ReflexionAgent(hipcortex)
exporter_agent = ExporterAgent(hipcortex)
monetizer_agent = MonetizerAgent(hipcortex)


# Dependency injection functions for agents
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


# In-memory store for latest test results and improvement suggestions
latest_test_results = {"success": None, "output": ""}
latest_improvement = {"suggestion": ""}


# Pydantic models for request bodies
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


# Root endpoint
@app.get("/")

async def root():
    return {"message": "Codex Booster Backend is running!"}

# Access control endpoint for restricted pages
import backend.auth.access_manager
from fastapi.responses import JSONResponse

@app.get("/restricted/page")
async def restricted_page():
    # Pass required arguments to check_access (user, page)
    access = backend.auth.access_manager.check_access(None, "restricted/page")
    if not access.get("access_granted", False):
        return JSONResponse(
            status_code=403,
            content={
                "access_granted": False,
                "redirect_url": access.get("redirect_url", "/login"),
                "warning_logged": access.get("warning_logged", True)
            }
        )
    return JSONResponse(
        status_code=200,
        content={"access_granted": True}
    )


# Direct API endpoints for agents (if you still use them directly)
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
    """Export an artifact and return archive path."""
    archive = agent.export(req.path)
    return {"archive": archive}


@app.get("/export/frontend")
async def export_frontend(agent: ExporterAgent = Depends(get_exporter_agent)):
    """Zip the frontend directory and return it as a download."""
    archive = agent.export("frontend")
    return FileResponse(archive, filename=Path(archive).name)


# Router-specific endpoints (these are likely what you're using for your UI)
@project_plan_router.post("/plan") # Assuming this is architect_router
async def plan_architecture(
    req: PlanRequest, agent: ArchitectAgent = Depends(get_architect_agent)
):
    """Return an architecture plan for the provided goal."""
    return agent.plan(req.goal)


@code_builder_router.post("/build") # Assuming this is builder_router
async def build_code(req: BuildRequest, agent: BuilderAgent = Depends(get_builder_agent)):
    """Generate code from tests."""
    code = agent.build(req.tests)
    return {"code": code}


@code_builder_router.post("/build_and_test")
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


@run_test_router.post("/run") # Assuming this is tester_router
async def run_tests_endpoint(
    req: RunTestsRequest, agent: TesterAgent = Depends(get_tester_agent)
):
    """Run tests against provided code."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        (tmp_path / "generated_module.py").write_text(req.code)
        (tmp_path / "test_generated.py").write_text(req.tests)
        success = agent.run_tests(tmpdir)
    return {"success": success, "output": agent.last_output}


@improvement_router.post("/reflect") # Assuming this is reflexion_router
async def reflect_endpoint(
    req: ReflexRequest, agent: ReflexionAgent = Depends(get_reflexion_agent)
):
    """Provide reflexion feedback."""
    instructions = agent.reflect(req.feedback)
    return {"instructions": instructions}


@exporter_router.post("/export")
async def export_endpoint(
    req: ExportRequest, agent: ExporterAgent = Depends(get_exporter_agent)
):
    """Export an artifact and return archive path."""
    archive = agent.export(req.path)
    return {"archive": archive}


@payment_router.post("/charge") # Assuming this is monetizer_router
async def charge_endpoint(
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


# Include all routers
app.include_router(hipcortex_router, prefix="/hipcortex")

# Create the MCP router by passing the initialized dependencies
mcp_router_instance = create_mcp_router(
    hipcortex_bridge=hipcortex,
    architect_agent=architect_agent,
    builder_agent=builder_agent,
    tester_agent=tester_agent,
    # Pass other agents here if you expose them via MCP
)
app.include_router(mcp_router_instance, prefix="/api") # MCP router (e.g., /api/mcp/tool)

# Include your other routers
app.include_router(marketplace_router)
app.include_router(doc_router)
app.include_router(chat_router)
app.include_router(config_router)
app.include_router(repo_init_router)
app.include_router(test_suite_router)
app.include_router(deploy_router)
app.include_router(terminal_runner_router)
app.include_router(auth_router)

# Note: The following routers are likely already included via the specific agent routers above
# app.include_router(architect_router) # Covered by project_plan_router
# app.include_router(builder_router)   # Covered by code_builder_router
# app.include_router(tester_router)    # Covered by run_test_router
# app.include_router(reflexion_router) # Covered by improvement_router
# app.include_router(exporter_router)  # Covered by exporter_router
# app.include_router(monetizer_router) # Covered by payment_router
