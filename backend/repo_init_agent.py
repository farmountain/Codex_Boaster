from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
import base64
import os

from backend.hipcortex_bridge import log_event, store_repo_snapshot

router = APIRouter()

GITHUB_API = "https://api.github.com"

GITHUB_CI_TEMPLATE = """
name: Codex Booster CI/CD

on:
  push:
    branches: [ 'main' ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.10
      - name: Install backend
        run: pip install -r backend/requirements.txt
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: 18
      - name: Install frontend
        run: |
          cd frontend
          npm ci
      - name: Run tests
        run: |
          pytest
          cd frontend && npm test
      - name: Deploy
        run: |
          curl -X POST https://your-deploy-endpoint/api/deploy \
               -H 'Authorization: Bearer ${{ secrets.CI_TOKEN }}'
""".strip()

GITLAB_CI_TEMPLATE = """
stages:
  - test
  - build
  - deploy

build:
  script:
    - pip install -r backend/requirements.txt
    - cd frontend && npm install

test:
  script:
    - pytest
    - cd frontend && npm test

deploy:
  script:
    - curl -X POST https://your-deploy-endpoint/api/deploy
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
        workflow_path = ".github/workflows/codex_booster.yml"
        ci_content = GITHUB_CI_TEMPLATE
        push_file(owner, req.project_name, workflow_path, ci_content, headers)
    elif req.ci == "gitlab":
        ci_content = GITLAB_CI_TEMPLATE
        push_file(owner, req.project_name, ".gitlab-ci.yml", ci_content, headers)

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


def scaffold_cicd(repo_path: str, provider: str = "github") -> None:
    """Write CI/CD templates into a local repository path."""
    if provider == "github":
        ci_path = os.path.join(repo_path, ".github", "workflows")
        os.makedirs(ci_path, exist_ok=True)
        with open(os.path.join(ci_path, "codex_booster.yml"), "w") as f:
            f.write(GITHUB_CI_TEMPLATE)
    elif provider == "gitlab":
        with open(os.path.join(repo_path, ".gitlab-ci.yml"), "w") as f:
            f.write(GITLAB_CI_TEMPLATE)
