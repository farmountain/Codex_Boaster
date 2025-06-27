from pathlib import Path
import tempfile

from backend.agents.builder_agent import BuilderAgent
from backend.agents.tester_agent import TesterAgent
from backend.agents.reflexion_agent import ReflexionAgent


def build_test_cycle(tests: str, builder: BuilderAgent, tester: TesterAgent, reflexion: ReflexionAgent):
    """Run build and test cycle with optional reflexion on failure."""
    code = builder.build(tests)
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        (tmp_path / "generated_module.py").write_text(code)
        (tmp_path / "test_generated.py").write_text(tests)
        success = tester.run_tests(tmpdir)
    if not success:
        feedback = tester.last_output
        instructions = reflexion.reflect(feedback)
        builder.update_instructions(instructions)
    return success, code
