"""Deployment agent for provisioning preview environments."""

from fastapi import APIRouter
from pydantic import BaseModel
import subprocess
from typing import Optional

from backend.hipcortex_bridge import log_event, store_deploy_snapshot

router = APIRouter()


class DeployRequest(BaseModel):
    runtime: str  # "node", "python", "nextjs"
    platform: str  # "vercel", "render", "fly"
    project_name: str
    token: str  # platform specific token
    repo_url: Optional[str] = None


@router.post("/deploy")
async def deploy(req: DeployRequest):
    """Deploy project artifacts using the selected platform."""
    try:
        log_event("DeployAgent", req.dict())

        if req.platform == "vercel":
            command = f"vercel --token {req.token} --yes"
        elif req.platform == "render":
            command = f"./scripts/render_deploy.sh {req.project_name} {req.token}"
        else:
            return {"error": "Unsupported platform"}

        result = subprocess.run(
            command, shell=True, capture_output=True, text=True
        )
        success = result.returncode == 0
        output = result.stdout
        error = result.stderr

        snapshot_id = store_deploy_snapshot(
            {
                "platform": req.platform,
                "project": req.project_name,
                "output": output,
                "success": success,
            }
        )

        return {
            "status": "success" if success else "failed",
            "output": output,
            "error": error,
            "snapshot_id": snapshot_id,
        }

    except Exception as e:  # pragma: no cover - unexpected failures
        return {"error": str(e)}, 500

