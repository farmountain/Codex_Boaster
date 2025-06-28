from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict

from backend.llm_client import generate_docs
from backend.hipcortex_bridge import log_event, store_doc_snapshot

router = APIRouter()

class DocRequest(BaseModel):
    files: Dict[str, str]
    context: Dict = {}

@router.post("/docs")
async def generate_documentation(req: DocRequest):
    try:
        documentation = generate_docs(req.files, req.context)
        snapshot_id = store_doc_snapshot(req.files, documentation)
        log_event("DocAgent", {"files": list(req.files.keys())})
        return {"documentation": documentation, "snapshot_id": snapshot_id}
    except Exception as e:  # pragma: no cover - unexpected failures
        return {"error": str(e)}, 500
