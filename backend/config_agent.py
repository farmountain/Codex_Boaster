from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, List

from backend.hipcortex_bridge import store_env_snapshot, log_event

router = APIRouter()


class EnvConfig(BaseModel):
    runtimes: Dict[str, str]
    env_vars: Dict[str, str]
    setup_script: List[str]


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
