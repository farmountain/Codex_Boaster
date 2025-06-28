from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from .llm_client import generate_code_snippet
from .hipcortex_bridge import log_event, store_code_snapshot

router = APIRouter()

class CodeInstruction(BaseModel):
    file_name: str
    purpose: str
    language: str
    context: str = ""

@router.post("/builder")
async def build_code(instructions: List[CodeInstruction]):
    results = []

    for inst in instructions:
        full_code = generate_code_snippet(inst.language, inst.purpose, inst.context)
        results.append({
            "file_name": inst.file_name,
            "language": inst.language,
            "content": full_code,
        })

    log_event("BuilderAgent", {"instructions": [i.dict() for i in instructions]})
    snapshot_id = store_code_snapshot(results)

    return {
        "status": "ok",
        "files": results,
        "snapshot_id": snapshot_id,
    }
