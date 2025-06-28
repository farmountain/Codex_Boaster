from fastapi import APIRouter, WebSocket
from pydantic import BaseModel
import subprocess
from pathlib import Path
from datetime import datetime
import os

from backend.hipcortex_bridge import log_runtime_command

LOG_DIR = Path("logs/runtime")
LOG_DIR.mkdir(parents=True, exist_ok=True)

router = APIRouter()

class SetupCommandRequest(BaseModel):
    commands: list[str]

@router.post("/run-setup")
def run_setup_script(request: SetupCommandRequest):
    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    log_path = LOG_DIR / f"{timestamp}.log"
    output = []
    with log_path.open("w") as lf:
        for cmd in request.commands:
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
async def ws_run_setup(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive_json()
    commands = data.get("commands", [])
    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    log_path = LOG_DIR / f"{timestamp}.log"
    with log_path.open("w") as lf:
        for cmd in commands:
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

