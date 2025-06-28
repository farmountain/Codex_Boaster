from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from backend.llm_client import generate_test_cases
from backend.hipcortex_bridge import log_event

router = APIRouter()

class TestGenRequest(BaseModel):
    file_name: str
    code: str
    test_type: str = "unit"  # or "uat", "integration"

@router.post("/generate-tests")
async def generate_tests(req: TestGenRequest):
    test_code = generate_test_cases(req.code, req.test_type)
    log_event(
        "TestSuiteAgent",
        {"file": req.file_name, "type": req.test_type, "test_code": test_code},
    )
    return {"test_code": test_code}
