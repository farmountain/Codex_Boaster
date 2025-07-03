"""Deployment agent for provisioning preview environments."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import subprocess
import requests
from typing import Optional

from backend.hipcortex_bridge import log_event, store_deploy_snapshot
from backend.services.secrets import get_secret

router = APIRouter()

latest_deploy_status = {"status": "idle", "logs": ""}


class DeployRequest(BaseModel):
    """Input payload for deployment."""

    project_name: str
    repo_url: str
    provider: str = "vercel"  # "vercel" or "fly"
    framework: str | None = None


class RollbackRequest(BaseModel):
    provider: str = "vercel"
    deployment_id: str
    project_name: str


VERCEL_API = "https://api.vercel.com"


def _detect_framework(repo: str) -> str:
    """Very naive framework detection based on repo url."""
    lower = repo.lower()
    if "next" in lower:
        return "nextjs"
    if "node" in lower:
        return "node"
    if "python" in lower:
        return "python"
    return "nextjs"


@router.post("/api/deploy")
async def deploy_app(req: DeployRequest):
    """Deploy the given repository using a provider."""

    provider = req.provider.lower()
    framework = req.framework or _detect_framework(req.repo_url)

    latest_deploy_status["status"] = "pending"
    latest_deploy_status["logs"] = ""

    log_event("DeployAgent", {
        "action": "deploy",
        "provider": provider,
        "project": req.project_name,
        "repo": req.repo_url,
    })

    if provider == "vercel":
        token = get_secret("VERCEL_TOKEN")
        if not token:
            raise HTTPException(status_code=500, detail="Missing Vercel API token")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        payload = {
            "name": req.project_name,
            "gitRepository": {
                "type": "github",
                "repo": req.repo_url,
            },
            "framework": framework,
        }
        try:
            res = requests.post(f"{VERCEL_API}/v13/deployments", headers=headers, json=payload)
            res.raise_for_status()
            data = res.json()
            deployment_url = data.get("url", "")
            result = {
                "status": "success",
                "deployment_url": deployment_url,
                "logs_url": f"https://vercel.com/dashboard/project/{req.project_name}/logs",
                "message": "Deployment triggered successfully.",
            }
        except Exception as e:  # pragma: no cover - network failure
            raise HTTPException(status_code=500, detail=f"Vercel deployment failed: {e}")
    elif provider == "fly":
        token = get_secret("FLY_API_TOKEN")
        if not token:
            raise HTTPException(status_code=500, detail="Missing Fly.io API token")
        command = f"flyctl deploy --remote-only --access-token {token}"
        proc = subprocess.run(command, shell=True, capture_output=True, text=True)
        success = proc.returncode == 0
        result = {
            "status": "success" if success else "failed",
            "deployment_url": "",
            "logs_url": "",
            "message": proc.stdout.strip(),
        }
        if not success:
            raise HTTPException(status_code=500, detail=proc.stderr)
    else:
        raise HTTPException(status_code=400, detail="Unsupported deployment provider")

    snapshot_id = store_deploy_snapshot({
        "provider": provider,
        "project": req.project_name,
        "result": result,
    })
    result["snapshot_id"] = snapshot_id
    latest_deploy_status["status"] = result.get("status", "unknown")
    latest_deploy_status["logs"] = result.get("message", "")
    return result


@router.post("/api/deploy/rollback")
async def rollback(req: RollbackRequest):
    """Rollback/cancel a deployment."""
    provider = req.provider.lower()
    log_event("DeployAgent", {"action": "rollback", "provider": provider, "deployment_id": req.deployment_id})

    if provider == "vercel":
        token = get_secret("VERCEL_TOKEN")
        if not token:
            raise HTTPException(status_code=500, detail="Missing Vercel API token")
        headers = {"Authorization": f"Bearer {token}"}
        try:
            res = requests.delete(f"{VERCEL_API}/v13/deployments/{req.deployment_id}", headers=headers)
            res.raise_for_status()
            return {"status": "rolled_back"}
        except Exception as e:  # pragma: no cover - network failure
            raise HTTPException(status_code=500, detail=f"Rollback failed: {e}")
    elif provider == "fly":
        token = get_secret("FLY_API_TOKEN")
        if not token:
            raise HTTPException(status_code=500, detail="Missing Fly.io API token")
        command = f"flyctl releases rollback -y {req.deployment_id} --access-token {token}"
        proc = subprocess.run(command, shell=True, capture_output=True, text=True)
        if proc.returncode == 0:
            return {"status": "rolled_back"}
        raise HTTPException(status_code=500, detail=proc.stderr)
    else:
        raise HTTPException(status_code=400, detail="Unsupported deployment provider")


@router.get("/api/deploy/status")
def deploy_status():
    """Return latest deployment status and logs."""
    return latest_deploy_status
