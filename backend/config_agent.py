from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Dict, List
import json
import os
import yaml
import requests

from backend.hipcortex_bridge import store_env_snapshot, log_event, set_runtime_context
from backend.agents.reflexion_agent import ReflexionAgent
from backend.integrations.hipcortex_bridge import HipCortexBridge

router = APIRouter()

CONFIG_PATH = "codexbooster.config.json"
ENV_TEMPLATE = ".env.template.json"
ENV_FILE = ".env"
DOCKER_COMPOSE = "docker-compose.yml"
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY")

class RuntimeConfig(BaseModel):
    python: str
    node: str
    rust: str

class LanguageVersion(BaseModel):
    language: str
    version: str

class EnvVar(BaseModel):
    key: str
    value: str

class EnvRequest(BaseModel):
    env: List[EnvVar]

class EnvConfig(BaseModel):
    runtimes: Dict[str, str]
    env_vars: Dict[str, str]
    setup_script: List[str] = Field(default_factory=list)
    llm_services: List[str] = Field(default_factory=list)


class PreRunValidator:
    """Simple validator hooked into ReflexionAgent."""

    def __init__(self) -> None:
        self.reflex = ReflexionAgent(HipCortexBridge(os.getenv("HIPCORTEX_URL", "http://hipcortex")))

    def validate(self, config: EnvConfig) -> str:
        missing = []
        if os.path.exists(ENV_TEMPLATE):
            with open(ENV_TEMPLATE) as f:
                schema = json.load(f)
            for key in schema.keys():
                if not config.env_vars.get(key):
                    missing.append(key)
        if missing:
            feedback = "Missing env vars: " + ", ".join(missing)
            return self.reflex.reflect(feedback)
        return ""


def _store_remote(data: dict) -> None:
    """Persist configuration in Supabase if credentials are present."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        return
    try:
        requests.post(
            f"{SUPABASE_URL}/rest/v1/config",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json",
            },
            json=data,
            timeout=5,
        )
    except requests.RequestException:
        pass


def _write_env_file(env_vars: Dict[str, str]) -> None:
    with open(ENV_FILE, "w") as f:
        for k, v in env_vars.items():
            f.write(f"{k}={v}\n")


def _write_config(config: EnvConfig) -> None:
    full_config = {}
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            full_config = json.load(f)
    full_config["runtime"] = config.runtimes
    with open(CONFIG_PATH, "w") as f:
        json.dump(full_config, f, indent=2)
    set_runtime_context(config.runtimes)


def _write_template(env_vars: Dict[str, str]) -> None:
    with open(ENV_TEMPLATE, "w") as f:
        json.dump({k: "" for k in env_vars.keys()}, f, indent=2)


def _write_docker_compose(config: EnvConfig) -> None:
    services = {
        "app": {
            "build": ".",
            "volumes": ["./:/app"],
            "ports": ["3000:3000"],
            "environment": list(config.env_vars.keys()),
            "command": "python3 -m uvicorn backend.main:app --reload",
        }
    }
    for svc in config.llm_services:
        services[svc] = {"image": svc.lower(), "restart": "always"}
    compose = {"version": "3", "services": services}
    with open(DOCKER_COMPOSE, "w") as f:
        yaml.dump(compose, f)


@router.get("/api/config/env")
async def read_env():
    envs = []
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE) as f:
            for line in f:
                if "=" in line and not line.strip().startswith("#"):
                    key, val = line.strip().split("=", 1)
                    envs.append({"key": key, "value": val})
    return envs


@router.post("/api/config/env")
async def write_env(req: EnvRequest):
    with open(ENV_FILE, "w") as f:
        for item in req.env:
            f.write(f"{item.key}={item.value}\n")
    return {"status": "updated"}


@router.get("/runtime-config", response_model=RuntimeConfig)
def get_runtime_config():
    if not os.path.exists(CONFIG_PATH):
        return RuntimeConfig(python="3.11", node="18", rust="1.72")
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


@router.post("/api/config/runtime")
def set_single_runtime(cfg: LanguageVersion):
    """Update a single language runtime."""
    full_config = {}
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            full_config = json.load(f)
    runtimes = full_config.get("runtime", {})
    runtimes[cfg.language.lower()] = cfg.version
    full_config["runtime"] = runtimes
    with open(CONFIG_PATH, "w") as f:
        json.dump(full_config, f, indent=2)
    set_runtime_context(runtimes)
    return {"message": f"Runtime set to {cfg.language} {cfg.version}"}


@router.post("/configure-env")
async def configure_environment(config: EnvConfig):
    """Persist environment configuration and provide reflexion feedback."""
    _write_env_file(config.env_vars)
    _write_config(config)
    _write_template(config.env_vars)
    _write_docker_compose(config)
    _store_remote(config.dict())

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

    validator = PreRunValidator()
    reflex = validator.validate(config)
    return {
        "message": "Environment configured successfully",
        "snapshot_id": snapshot_id,
        "reflexion": reflex,
    }
