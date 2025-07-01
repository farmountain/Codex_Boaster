from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import json
import os

router = APIRouter()

# JSON file used to persist plugin metadata. Path can be patched in tests.
PLUGIN_STORE = "plugins.json"


class Plugin(BaseModel):
    """Metadata describing a marketplace plugin."""

    plugin_id: str
    name: str
    type: str
    entrypoint: str
    capabilities: List[str]
    version: str
    enabled: bool = True


@router.post("/api/marketplace/register")
async def register_plugin(plugin: Plugin):
    """Register a new plugin in the local store."""
    plugins = _load_plugins()
    if any(p["plugin_id"] == plugin.plugin_id for p in plugins):
        raise HTTPException(status_code=400, detail="Plugin already registered")

    plugins.append(plugin.dict())
    _save_plugins(plugins)
    return {"status": "success", "message": "Plugin registered"}


@router.get("/api/marketplace")
async def list_plugins() -> List[Plugin]:
    """Return all registered plugins."""
    return _load_plugins()


@router.post("/api/marketplace/toggle/{plugin_id}")
async def toggle_plugin(plugin_id: str):
    """Enable or disable a plugin by ID."""
    plugins = _load_plugins()
    for p in plugins:
        if p["plugin_id"] == plugin_id:
            p["enabled"] = not p.get("enabled", True)
            _save_plugins(plugins)
            return {"status": "success", "enabled": p["enabled"]}
    raise HTTPException(status_code=404, detail="Plugin not found")


def _load_plugins() -> List[dict]:
    """Load plugins from PLUGIN_STORE."""
    if not os.path.exists(PLUGIN_STORE):
        return []
    with open(PLUGIN_STORE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_plugins(data: List[dict]) -> None:
    """Persist plugin data to PLUGIN_STORE."""
    with open(PLUGIN_STORE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
