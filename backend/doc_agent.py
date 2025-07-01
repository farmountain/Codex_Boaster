from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import os

from backend.hipcortex_bridge import log_event, store_doc_snapshot, get_reflexion_logs

router = APIRouter()

class DocRequest(BaseModel):
    project_name: str
    log_source: str = "hipcortex"
    format: str = "markdown"
    include_code: bool = True
    sections: List[str] = ["summary", "architecture", "agent_flow"]

@router.post("/api/docs")
async def generate_docs(req: DocRequest):
    """Return generated markdown documentation for a project."""
    try:
        logs = get_logs_from_source(req.log_source)
        summary = summarize_logs(logs, sections=req.sections)
        code_snippets = extract_code(logs) if req.include_code else ""

        md = f"# {req.project_name}\n\n"
        if "summary" in req.sections:
            md += f"## Summary\n{summary.get('summary', '')}\n\n"
        if "agent_flow" in req.sections:
            md += f"## Agent Flow\n{summary.get('agent_flow', '')}\n\n"
        if "architecture" in req.sections:
            md += f"## Architecture\n{summary.get('architecture', '')}\n\n"
        if code_snippets:
            md += f"## Code Examples\n```python\n{code_snippets}\n```\n"

        store_doc_snapshot({"logs": logs}, md)
        log_event("DocAgent", {"source": req.log_source, "sections": req.sections})
        return {"status": "success", "markdown": md}
    except Exception as e:  # pragma: no cover - unexpected failures
        raise HTTPException(status_code=500, detail=str(e))

def get_logs_from_source(source: str):
    """Retrieve logs from the configured source."""
    if source == "hipcortex":
        try:
            raw = get_reflexion_logs()
            return [f"[{e.get('agent')}] {e.get('log')}" for e in raw]
        except Exception:
            return []
    log_dir = os.path.join("logs", source)
    if os.path.isdir(log_dir):
        lines = []
        for fname in os.listdir(log_dir):
            with open(os.path.join(log_dir, fname)) as fh:
                lines.extend([l.strip() for l in fh.readlines()])
        return lines
    return [
        "[ArchitectAgent] Planned repo with CI",
        "[BuilderAgent] Generated main.py",
        "[ReflexionAgent] Feedback: Add validation",
        "Generated code: def hello(): print('Hi')",
    ]

def summarize_logs(logs, sections):
    """Create a very small summary dictionary from log lines."""
    flow = []
    for line in logs:
        if "ArchitectAgent" in line and "ArchitectAgent" not in " ".join(flow):
            flow.append("ArchitectAgent")
        if "BuilderAgent" in line and "BuilderAgent" not in " ".join(flow):
            flow.append("BuilderAgent")
        if "ReflexionAgent" in line and "ReflexionAgent" not in " ".join(flow):
            flow.append("ReflexionAgent")
    return {
        "summary": "This project was planned, built, and refined using Codex Booster's agent loop.",
        "agent_flow": " -> ".join(flow),
        "architecture": "Uses FastAPI backend, Next.js frontend, Codex orchestration loop",
    }

def extract_code(logs):
    """Extract the last python code block from the logs if available."""
    for line in reversed(logs):
        if line.strip().startswith("def ") or line.strip().startswith("class "):
            return line.strip()
        if line.startswith("Generated code:"):
            return line.split("Generated code:", 1)[-1].strip()
    return ""
