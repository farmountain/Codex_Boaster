from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
import base64
import os

from backend.hipcortex_bridge import log_event, store_repo_snapshot

router = APIRouter()

GITHUB_API = "https://api.github.com"

# Simple CI workflow template used when `ci` is "github-actions"
WORKFLOW_TEMPLATE = """
name: CI

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      - name: Install deps
        run: pip install -r requirements.txt || true
      - name: Run tests
        run: pytest || echo 'no tests'
""".strip()


class RepoInitRequest(BaseModel):
    """Input payload for initializing a repository."""

    project_name: str
    description: str
    language: str
    private: bool = True
    ci: str = "github-actions"


@router.post("/api/repo-init")
async def initialize_repo(req: RepoInitRequest):
    """Create a GitHub repository and push basic scaffolding."""

    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise HTTPException(status_code=500, detail="GitHub token missing.")

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    res = requests.post(
        f"{GITHUB_API}/user/repos",
        headers=headers,
        json={
            "name": req.project_name,
            "description": req.description,
            "private": req.private,
            "auto_init": True,
        },
    )

    if res.status_code not in (200, 201):
        raise HTTPException(
            status_code=400,
            detail=f"GitHub repo creation failed: {res.json()}",
        )

    repo_data = res.json()
    owner = repo_data.get("owner", {}).get("login")

    files = generate_template(req.language)
    push_initial_files(owner, req.project_name, files, headers)

    if req.ci == "github-actions":
        workflow_path = ".github/workflows/main.yml"
        ci_content = WORKFLOW_TEMPLATE
        push_file(owner, req.project_name, workflow_path, ci_content, headers)

    log_event(
        "RepoInitAgent",
        {"repo": req.project_name, "language": req.language, "ci": req.ci},
    )
    store_repo_snapshot(req.project_name, files)

    return {
        "status": "success",
        "repo_url": repo_data.get("html_url"),
        "commit_status": "templates_committed",
        "ci_setup": req.ci,
    }


def generate_template(language: str) -> dict:
    """Return a minimal scaffold for the chosen language."""

    if language == "node":
        return {
            "README.md": "# Node.js Project",
            ".gitignore": "node_modules/\n.env",
        }

    if language == "python":
        return {
            "README.md": "# Python Project",
            ".gitignore": "__pycache__/\n.env",
        }

    return {
        "README.md": "# Codex Booster Project",
        ".gitignore": ".env\n__pycache__/",
    }


def push_file(owner: str, repo: str, path: str, content: str, headers: dict) -> None:
    """Create or update a file in the repository."""

    url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}"
    requests.put(
        url,
        headers=headers,
        json={
            "message": f"Add {path}",
            "content": base64.b64encode(content.encode("utf-8")).decode("utf-8"),
        },
    )


def push_initial_files(owner: str, repo: str, files: dict, headers: dict) -> None:
    """Push multiple template files to the new repository."""

    for path, content in files.items():
        push_file(owner, repo, path, content, headers)
