from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class MarketplaceItem(BaseModel):
    name: str
    type: str  # e.g., "LLM", "RAG", "Database", "Analytics"
    description: str
    endpoint: str
    icon_url: str
    requires_api_key: bool
    is_installed: bool = False

mock_db = [
    MarketplaceItem(
        name="Ollama LLM",
        type="LLM",
        description="Local LLM runner with API",
        endpoint="http://localhost:11434",
        icon_url="/icons/ollama.png",
        requires_api_key=False
    ),
    MarketplaceItem(
        name="Supabase DB",
        type="Database",
        description="Postgres with auth and REST API",
        endpoint="https://xyz.supabase.co",
        icon_url="/icons/supabase.png",
        requires_api_key=True
    )
]

@router.get("/marketplace", response_model=List[MarketplaceItem])
def list_plugins():
    return mock_db

@router.post("/marketplace/install")
def install_plugin(item: MarketplaceItem):
    # Save to project config or memory
    from backend.hipcortex_bridge import log_event
    log_event("MarketplaceService", {
        "action": "install",
        "plugin": item.name,
        "endpoint": item.endpoint
    })
    return { "message": f"{item.name} installed." }
