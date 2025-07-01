from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, List

from backend.llm_client import generate_test_cases
from backend.hipcortex_bridge import log_event

router = APIRouter()

def scenarios_to_markdown(scenarios: List[Dict]) -> str:
    """Convert UAT scenarios to markdown format."""
    lines = []
    for s in scenarios:
        lines.append(f"### {s['title']}")
        for i, step in enumerate(s['steps'], 1):
            lines.append(f"{i}. {step}")
        lines.append(f"**Expected:** {s['expected']}")
        lines.append("")
    return "\n".join(lines)

class TestGenRequest(BaseModel):
    file_name: str
    code: str
    test_type: str = "unit"  # or "uat", "integration"


class TestSuiteRequest(BaseModel):
    business_description: str
    language: str = "python"
    framework: str = "pytest"


class UATScenario(BaseModel):
    title: str
    steps: List[str]
    expected: str


class TestSuiteResponse(BaseModel):
    unit_tests: Dict[str, str]
    sit_tests: Dict[str, str]
    uat_scenarios: List[UATScenario]
    uat_markdown: str | None = None

@router.post("/generate-tests")
async def generate_tests(req: TestGenRequest):
    test_code = generate_test_cases(req.code, req.test_type)
    log_event(
        "TestSuiteAgent",
        {"file": req.file_name, "type": req.test_type, "test_code": test_code},
    )
    return {"test_code": test_code}


@router.post("/api/test-suite", response_model=TestSuiteResponse)
async def generate_test_suite(req: TestSuiteRequest):
    """Return unit, SIT and UAT artefacts derived from a business description."""

    unit_code = generate_test_cases(req.business_description, "unit")
    sit_code = generate_test_cases(req.business_description, "integration")

    unit_tests = {"test_register_user.py": unit_code}
    sit_tests = {"test_user_flow.py": sit_code}

    uat_scenarios = [
        {
            "title": "User logs in with Google",
            "steps": [
                "Navigate to login page",
                "Click 'Sign in with Google'",
                "Grant permission",
                "Redirect to dashboard",
            ],
            "expected": "User is logged in and sees the dashboard",
        }
    ]
    uat_markdown = scenarios_to_markdown(uat_scenarios)

    log_event(
        "TestSuiteAgent",
        {
            "description": req.business_description,
            "unit_files": list(unit_tests.keys()),
            "sit_files": list(sit_tests.keys()),
        },
    )

    return {
        "unit_tests": unit_tests,
        "sit_tests": sit_tests,
        "uat_scenarios": uat_scenarios,
        "uat_markdown": uat_markdown,
    }
