import asyncio
import json
import os
import tempfile
from datetime import datetime
from pathlib import Path

from backend.agents.builder_agent import BuilderAgent
from backend.agents.tester_agent import TesterAgent
from backend.agents.reflexion_agent import ReflexionAgent
from backend.agents.exporter_agent import ExporterAgent
from backend.integrations.hipcortex_bridge import HipCortexBridge
from backend.supabase_connector import SupabaseClient
from backend.llm_client import generate_test_cases


class CodexAgent:
    """Orchestrate a reflexive build and test loop."""

    def __init__(self, hipcortex_url: str | None = None) -> None:
        self.hipcortex = HipCortexBridge(base_url=hipcortex_url or "http://hipcortex")
        supa_url = os.getenv("SUPABASE_URL")
        supa_key = os.getenv("SUPABASE_KEY")
        self.supabase = SupabaseClient(supa_url, supa_key) if supa_url and supa_key else None
        self.builder = BuilderAgent(self.hipcortex)
        self.tester = TesterAgent(self.hipcortex)
        self.reflexion = ReflexionAgent(self.hipcortex)
        self.exporter = ExporterAgent(self.hipcortex)

    async def _log_run(self, data: dict) -> None:
        if not self.supabase:
            return
        try:
            await self.supabase.insert("prompt_runs", data)
        except Exception:
            pass

    def _run_tests(self, code: str, tests: str) -> bool:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir)
            (path / "generated_module.py").write_text(code)
            (path / "test_generated.py").write_text(tests)
            return self.tester.run_tests(tmpdir)

    async def run_pipeline(self, goal: str) -> dict:
        """Execute build/test/reflexion loop until success or max retries."""
        tests = generate_test_cases(goal, "unit") + "\n" + generate_test_cases(goal, "integration")
        attempt = 0
        success = False
        logs: list[dict] = []

        while attempt < 3 and not success:
            code = self.builder.build(tests)
            success = self._run_tests(code, tests)
            row = {
                "goal": goal,
                "attempt": attempt + 1,
                "success": success,
                "confidence": 1.0 if success else 0.5,
                "tokens": len(code) + len(tests),
            }
            await self._log_run(row)
            logs.append(row)
            if not success:
                instructions = self.reflexion.reflect(self.tester.last_output)
                self.builder.update_instructions(instructions)
            attempt += 1

        log_dir = Path("reflexion_logs")
        log_dir.mkdir(exist_ok=True)
        ts = int(datetime.utcnow().timestamp())
        log_file = log_dir / f"uat_passed_{ts}.json"
        log_file.write_text(json.dumps(logs, indent=2))
        archive = self.exporter.export(str(log_file))
        return {"success": success, "log_file": str(log_file), "archive": archive}


async def run_cli() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Run Codex pipeline")
    parser.add_argument("goal")
    args = parser.parse_args()

    agent = CodexAgent()
    result = await agent.run_pipeline(args.goal)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(run_cli())
