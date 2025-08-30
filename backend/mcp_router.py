# backend/mcp_router.py
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, List

# Import necessary classes, but NOT from backend.main to avoid circular import
from backend.agents.builder_agent import BuilderAgent
from backend.agents.architect_agent import ArchitectAgent
from backend.agents.tester_agent import TesterAgent

# Import HipCortexBridge and models
from backend.integrations.hipcortex_bridge import HipCortexBridge
from backend.dashboard.models import AgentLogEntry, AgentConfidenceScore

# Define the models for MCP Tool Requests
class ToolInvocation(BaseModel):
    """Represents a request to invoke an MCP tool."""
    tool: str
    arguments: Dict[str, Any]
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional context from Copilot, e.g., sessionId, filePath.")

class ToolResponse(BaseModel):
    """Represents the response from an MCP tool."""
    content: str = Field(description="The primary output content, typically Markdown.")

# This function will create and return the APIRouter,
# receiving dependencies as arguments.
def create_mcp_router(
    hipcortex_bridge: HipCortexBridge,
    architect_agent: ArchitectAgent,
    builder_agent: BuilderAgent,
    tester_agent: TesterAgent,
    # Add other agents here if you expose them via MCP
):
    router = APIRouter()

    # The agents and hipcortex_bridge are now available directly via function arguments
    _hipcortex = hipcortex_bridge # Use the passed-in instance

    @router.post("/mcp/tool")
    async def invoke_mcp_tool(
        invocation: ToolInvocation,
    ):
        """
        Receives an MCP tool invocation request from GitHub Copilot.
        Dispatches the request to the appropriate Codex Booster agent.
        """
        tool_name = invocation.tool
        arguments = invocation.arguments
        current_context = invocation.context

        if tool_name == "codex_booster.builder":
            goal = arguments.get("goal")
            language = arguments.get("language", "python")
            
            if not goal:
                raise HTTPException(status_code=400, detail="Missing 'goal' argument for builder tool.")
            
            try:
                print(f"MCP Call: Builder Agent invoked with goal='{goal}', language='{language}'")
                # Use the passed-in builder_agent instance
                generated_code = builder_agent.build(goal) 

                session_id = current_context.get("sessionId", "copilot_default_session")
                log_entry = AgentLogEntry(
                    session_id=session_id,
                    agent_name="BuilderAgent_MCP_Invocation",
                    prompt_input=f"Goal: {goal}, Language: {language}",
                    output_content=generated_code,
                    confidence_score=AgentConfidenceScore(score=0.9, rationale="MCP tool successfully invoked Builder Agent and received code."),
                    context_info=current_context
                )
                await _hipcortex.record_snapshot(log_entry)

                return ToolResponse(content=generated_code)
            except Exception as e:
                print(f"ERROR: Builder Agent invocation failed: {e}")
                raise HTTPException(status_code=500, detail=f"Codex Booster Builder Agent failed: {str(e)}. Check backend logs for details.")

        elif tool_name == "codex_booster.architect":
            problem_statement = arguments.get("problem_statement")
            if not problem_statement:
                raise HTTPException(status_code=400, detail="Missing 'problem_statement' argument for architect tool.")
            
            try:
                print(f"MCP Call: Architect Agent invoked with problem_statement='{problem_statement}'")
                # Use the passed-in architect_agent instance
                architecture_plan = architect_agent.plan(problem_statement)
                
                session_id = current_context.get("sessionId", "copilot_default_session")
                log_entry = AgentLogEntry(
                    session_id=session_id,
                    agent_name="ArchitectAgent_MCP_Invocation",
                    prompt_input=problem_statement,
                    output_content=architecture_plan,
                    confidence_score=AgentConfidenceScore(score=0.95, rationale="MCP tool successfully invoked Architect Agent and received plan."),
                    context_info=current_context
                )
                await _hipcortex.record_snapshot(log_entry)

                return ToolResponse(content=architecture_plan)
            except Exception as e:
                print(f"ERROR: Architect Agent invocation failed: {e}")
                raise HTTPException(status_code=500, detail=f"Codex Booster Architect Agent failed: {str(e)}. Check backend logs for details.")

        elif tool_name == "codex_booster.tester":
            code_to_test = arguments.get("code")
            test_type = arguments.get("test_type", "unit")
            if not code_to_test:
                raise HTTPException(status_code=400, detail="Missing 'code' argument for tester tool.")
            
            try:
                print(f"MCP Call: Tester Agent invoked for code snippet with test_type='{test_type}'.")
                # Use the passed-in tester_agent instance
                from pathlib import Path
                import tempfile
                
                with tempfile.TemporaryDirectory() as tmpdir:
                    tmp_path = Path(tmpdir)
                    (tmp_path / "generated_module.py").write_text(code_to_test)
                    dummy_tests = "import unittest\nclass MyTests(unittest.TestCase):\n    def test_dummy(self):\n        self.assertTrue(True)\n"
                    (tmp_path / "test_generated.py").write_text(dummy_tests)
                    
                    success = tester_agent.run_tests(tmpdir)
                    test_results = tester_agent.last_output

                session_id = current_context.get("sessionId", "copilot_default_session")
                log_entry = AgentLogEntry(
                    session_id=session_id,
                    agent_name="TesterAgent_MCP_Invocation",
                    prompt_input=f"Code: {code_to_test[:100]}..., Test Type: {test_type}",
                    output_content=test_results,
                    confidence_score=AgentConfidenceScore(score=0.8, rationale="MCP tool successfully invoked Tester Agent and received results."),
                    context_info=current_context
                )
                await _hipcortex.record_snapshot(log_entry)

                return ToolResponse(content=test_results)
            except Exception as e:
                print(f"ERROR: Tester Agent invocation failed: {e}")
                raise HTTPException(status_code=500, detail=f"Codex Booster Tester Agent failed: {str(e)}. Check backend logs for details.")
        
        else:
            raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found.")

    # --- MCP Discovery Endpoint ---
    @router.get("/mcp/v1/tools")
    async def get_mcp_tools_manifest():
        """
        Returns the manifest of tools available on this MCP server.
        """
        return {
            "tools": [
                {
                    "name": "codex_booster.builder",
                    "description": "Generates code based on a natural language goal and programming language using Codex Booster's Builder Agent.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "goal": {
                                "type": "string",
                                "description": "The natural language goal describing the desired software functionality."
                            },
                            "language": {
                                "type": "string",
                                "description": "The programming language (e.g., 'python', 'javascript', 'rust').",
                                "enum": ["python", "javascript", "rust", "go", "java", "swift", "ruby", "bun", "node"]
                            }
                        },
                        "required": ["goal"]
                    }
                },
                {
                    "name": "codex_booster.architect",
                    "description": "Generates an architectural plan for a given software problem using Codex Booster's Architect Agent.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "problem_statement": {
                                "type": "string",
                                "description": "A detailed description of the software problem to solve."
                            }
                        },
                        "required": ["problem_statement"]
                    }
                },
                {
                    "name": "codex_booster.tester",
                    "description": "Analyzes and tests provided code for correctness and identifies issues using Codex Booster's Tester Agent.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "string",
                                "description": "The code snippet to be tested."
                            },
                            "test_type": {
                                "type": "string",
                                "description": "The type of test to perform (e.g., 'unit', 'integration').",
                                "enum": ["unit", "integration", "security", "performance"]
                            }
                        },
                        "required": ["code"]
                    }
                }
            ]
        }
    return router # Return the configured router
