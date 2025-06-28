from fastapi import APIRouter
from pydantic import BaseModel
import subprocess
from backend.hipcortex_bridge import log_event, store_test_results

router = APIRouter()

class TestRequest(BaseModel):
    runtime: str  # e.g., "python", "node"
    command: str = ""  # Optional override test command

@router.post("/run-tests")
async def run_tests(req: TestRequest):
    try:
        cmd = req.command or default_test_command(req.runtime)
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        output = result.stdout
        error = result.stderr
        success = result.returncode == 0

        test_log = {
            "runtime": req.runtime,
            "command": cmd,
            "success": success,
            "stdout": output,
            "stderr": error,
        }

        log_event("TesterAgent", test_log)
        snapshot_id = store_test_results(test_log)

        return {"success": success, "stdout": output, "stderr": error, "snapshot_id": snapshot_id}
    except Exception as e:  # pragma: no cover - unexpected failures
        return {"error": str(e)}, 500


def default_test_command(runtime: str) -> str:
    return {
        "python": "pytest -q",
        "node": "npm test",
    }.get(runtime, "echo 'No test runner configured'")
