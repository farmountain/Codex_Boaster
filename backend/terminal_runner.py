from fastapi import APIRouter, WebSocket, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict
import subprocess
from pathlib import Path
from datetime import datetime
import os
import uuid

from backend.hipcortex_bridge import log_runtime_command
from backend.security import require_role

ALLOWED_BINARIES = {
    "npm",
    "pip",
    "pytest",
    "python",
    "node",
    "echo",
    "ls",
    "pwd",
}


def _validate_command(cmd: str) -> None:
    binary = cmd.strip().split()[0]
    if binary not in ALLOWED_BINARIES:
        raise HTTPException(status_code=403, detail="Command not allowed")

LOG_DIR = Path("logs/runtime")
LOG_DIR.mkdir(parents=True, exist_ok=True)

router = APIRouter()

class SetupCommandRequest(BaseModel):
    commands: list[str]


class RunCommandRequest(BaseModel):
    """Request model for a single command run."""
    command: str
    cwd: str = "./"
    env: Dict[str, str] = {}


class RunCommandResponse(BaseModel):
    stdout: str
    stderr: str
    exit_code: int
    log_id: str


@router.post("/api/run-setup", response_model=RunCommandResponse)
async def run_single_command(
    req: RunCommandRequest, payload: dict = Depends(require_role("admin"))
):
    """Run a single shell command and return its output."""
    try:
        _validate_command(req.command)
        log_id = f"run-{uuid.uuid4().hex[:8]}"
        env = os.environ.copy()
        env.update(req.env)
        proc = subprocess.run(
            req.command,
            shell=True,
            capture_output=True,
            cwd=req.cwd,
            env=env,
            timeout=30,
        )

        log_path = LOG_DIR / f"{log_id}.log"
        with log_path.open("w") as lf:
            lf.write(f"$ {req.command}\n{proc.stdout.decode('utf-8')}{proc.stderr.decode('utf-8')}\n")

        status = "success" if proc.returncode == 0 else "error"
        log_runtime_command(req.command, status)

        return {
            "stdout": proc.stdout.decode("utf-8"),
            "stderr": proc.stderr.decode("utf-8"),
            "exit_code": proc.returncode,
            "log_id": log_id,
        }

    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=408, detail="Command timed out.")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/run-setup")
def run_setup_script(
    request: SetupCommandRequest, payload: dict = Depends(require_role("admin"))
):
    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    log_path = LOG_DIR / f"{timestamp}.log"
    output = []
    with log_path.open("w") as lf:
        for cmd in request.commands:
            _validate_command(cmd)
            try:
                result = subprocess.run(
                    cmd,
                    shell=True,
                    check=True,
                    capture_output=True,
                    text=True,
                )
                log_runtime_command(cmd, "success")
                lf.write(f"$ {cmd}\n{result.stdout}\n{result.stderr}\n")
                output.append(
                    {
                        "command": cmd,
                        "stdout": result.stdout,
                        "stderr": result.stderr,
                        "status": "success",
                    }
                )
            except subprocess.CalledProcessError as e:
                log_runtime_command(cmd, "error")
                lf.write(f"$ {cmd}\n{e.stdout}\n{e.stderr}\n")
                output.append(
                    {
                        "command": cmd,
                        "stdout": e.stdout,
                        "stderr": e.stderr,
                        "status": "error",
                    }
                )
    return {"results": output, "log_file": str(log_path)}

@router.websocket("/ws/run-setup")
async def ws_run_setup(websocket: WebSocket, payload: dict = Depends(require_role("admin"))):
    await websocket.accept()
    data = await websocket.receive_json()
    commands = data.get("commands", [])
    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    log_path = LOG_DIR / f"{timestamp}.log"
    with log_path.open("w") as lf:
        for cmd in commands:
            _validate_command(cmd)
            proc = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            for line in proc.stdout:
                await websocket.send_json({"command": cmd, "output": line})
                lf.write(line)
            proc.wait()
            status = "success" if proc.returncode == 0 else "error"
            log_runtime_command(cmd, status)
            await websocket.send_json({"command": cmd, "status": status})
    await websocket.close()

