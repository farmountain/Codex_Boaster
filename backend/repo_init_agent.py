from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
import base64

from backend.hipcortex_bridge import log_event, store_repo_snapshot

router = APIRouter()

GITHUB_API = "https://api.github.com"

class RepoInitInput(BaseModel):
    github_token: str
    github_user: str
    repo_name: str
    description: str
    visibility: str = "private"
    template: str = "default"

@router.post("/repo-init")
async def repo_init(input: RepoInitInput):
    headers = {
        "Authorization": f"token {input.github_token}",
        "Accept": "application/vnd.github.v3+json",
    }

    res = requests.post(
        f"{GITHUB_API}/user/repos",
        headers=headers,
        json={
            "name": input.repo_name,
            "description": input.description,
            "private": input.visibility == "private",
        },
    )

    if res.status_code not in (200, 201):
        raise HTTPException(
            status_code=400,
            detail=f"GitHub repo creation failed: {res.json()}",
        )

    scaffold = generate_template(input.template)
    push_initial_files(input, scaffold, headers)

    log_event(
        "RepoInitAgent",
        {"repo": input.repo_name, "template": input.template},
    )
    snapshot_id = store_repo_snapshot(input.repo_name, scaffold)
    return {"message": "Repo created", "snapshot_id": snapshot_id}


def generate_template(template: str) -> dict:
    if template == "node":
        return {
            "README.md": "# Node.js Project",
            ".gitignore": "node_modules/\n.env",
            ".github/workflows/ci.yml": "name: Node CI\non: [push]",
        }
    if template == "python":
        return {
            "README.md": "# Python Project",
            ".gitignore": "__pycache__/\n.env",
            ".github/workflows/ci.yml": "name: Python CI\non: [push]",
        }
    return {
        "README.md": "# Codex Booster Project",
        ".gitignore": ".env\n__pycache__/",
        ".github/workflows/ci.yml": "name: Basic CI\non: [push]",
    }


def push_initial_files(input: RepoInitInput, files: dict, headers: dict) -> None:
    for path, content in files.items():
        url = f"{GITHUB_API}/repos/{input.github_user}/{input.repo_name}/contents/{path}"
        requests.put(
            url,
            headers=headers,
            json={
                "message": f"Add {path}",
                "content": base64.b64encode(content.encode("utf-8")).decode("utf-8"),
            },
        )
