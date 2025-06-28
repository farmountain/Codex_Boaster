from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List
import json
import os

from backend.hipcortex_bridge import store_env_snapshot, log_event, set_runtime_context

router = APIRouter()

CONFIG_PATH = "codexbooster.config.json"


class RuntimeConfig(BaseModel):
    python: str
    node: str
    go: str


class EnvConfig(BaseModel):
    runtimes: Dict[str, str]
    env_vars: Dict[str, str]
    setup_script: List[str]


@router.get("/runtime-config", response_model=RuntimeConfig)
def get_runtime_config():
    if not os.path.exists(CONFIG_PATH):
        return RuntimeConfig(python="3.10", node="18", go="1.19")
    with open(CONFIG_PATH) as f:
        data = json.load(f)
        return RuntimeConfig(**data.get("runtime", {}))


@router.post("/runtime-config")
def save_runtime_config(config: RuntimeConfig):
    full_config = {}
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            full_config = json.load(f)
    full_config["runtime"] = config.dict()
    with open(CONFIG_PATH, "w") as f:
        json.dump(full_config, f, indent=2)
    set_runtime_context(config.dict())
    return {"message": "Runtime config saved."}


@router.post("/configure-env")
async def configure_environment(config: EnvConfig):
    """Persist environment configuration and log to HipCortex."""
    try:
        snapshot_id = store_env_snapshot(config.dict())
        log_event(
            "ConfigAgent",
            {
                "type": "env_config",
                "snapshot_id": snapshot_id,
                "runtimes": config.runtimes,
                "env_vars": list(config.env_vars.keys()),
            },
        )
        return {"message": "Environment configured successfully", "snapshot_id": snapshot_id}
    except Exception as e:  # pragma: no cover - unexpected failures
        return {"error": str(e)}, 500
