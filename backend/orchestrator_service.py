"""Standalone FastAPI service for orchestration and evaluation."""

import os
from typing import Any, Dict, Optional

from fastapi import Depends, FastAPI, HTTPException
from jinja2 import Template
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.database import Base, engine, get_db
from backend.database.models import Run
from backend.orchestration import ArtifactStorage, GuardrailPolicy, ReviewGate


# Initialise database
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Codex Orchestrator")

# Orchestration helpers
guardrails = GuardrailPolicy()
review_gate = ReviewGate()
artifact_storage = ArtifactStorage()


# ---------------------------------------------------------------------------
# RAG storage integration
# ---------------------------------------------------------------------------


class RAGStore:
    """Minimal wrapper around either Chroma or Weaviate."""

    def __init__(self) -> None:
        backend = os.getenv("RAG_BACKEND", "chroma").lower()
        if backend == "weaviate":
            import weaviate

            self.client = weaviate.Client(
                url=os.getenv("WEAVIATE_URL", "http://localhost:8080")
            )
            self.collection = "Prompts"
        else:
            import chromadb

            self.client = chromadb.PersistentClient(
                path=os.getenv("CHROMA_PATH", "./chroma_store")
            )
            self.collection = self.client.get_or_create_collection("prompts")

    def get_prompt(self, prompt_id: str) -> str:
        if hasattr(self, "collection") and hasattr(self.collection, "get"):
            result = self.collection.get(ids=[prompt_id])
            if result and result.get("documents"):
                return result["documents"][0]
        else:  # weaviate
            result = self.client.data_object.get_by_id(prompt_id, class_name=self.collection)
            if result and result.get("properties") and result["properties"].get("text"):
                return result["properties"]["text"]
        raise KeyError(f"Prompt {prompt_id} not found")


rag_store = RAGStore()


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class RunCreate(BaseModel):
    plan: str
    parameters: Optional[Dict[str, Any]] = None


class EvalRequest(BaseModel):
    run_id: int
    score: float
    notes: Optional[str] = None


# ---------------------------------------------------------------------------
# Endpoint implementations
# ---------------------------------------------------------------------------


@app.get("/plans")
def list_plans() -> Dict[str, Any]:
    """Return placeholder plans.

    In a real implementation these might be generated dynamically or retrieved
    from a planning service.
    """

    return {"plans": ["default"]}


@app.post("/runs")
def create_run(run: RunCreate, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Create a new run after applying guardrails and review gates."""

    try:
        guardrails.validate_plan(run.plan)
    except ValueError as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=400, detail=str(exc))

    db_run = Run(plan=run.plan, status="created")
    db.add(db_run)
    db.commit()
    db.refresh(db_run)

    # Artifact storage example
    artifact_storage.save_text(db_run.id, "input.json", run.json())

    # Review gate – currently a no-op but keeps structure for future logic
    review_gate.approve(db_run)

    return {"run_id": db_run.id, "status": db_run.status}


@app.get("/prompts/{prompt_id}/render")
def render_prompt(prompt_id: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Render a prompt template retrieved from the RAG store."""

    template_text = rag_store.get_prompt(prompt_id)
    template = Template(template_text)
    rendered = template.render(**(variables or {}))
    return {"prompt": rendered}


@app.post("/eval/run")
def eval_run(req: EvalRequest, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Record evaluation metadata for a run."""

    run = db.query(Run).filter(Run.id == req.run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    # For demonstration we store evaluation as an artifact
    artifact_storage.save_text(run.id, "evaluation.json", req.json())

    run.status = "evaluated"
    db.add(run)
    db.commit()

    return {"run_id": run.id, "status": run.status}


__all__ = ["app"]

