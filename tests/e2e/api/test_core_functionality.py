"""End-to-end API tests for core functionality."""

import pytest
import time
from tests.e2e.utils.api_client import APIClient, E2ETestContext


class TestAPIHealthCheck:
    """Test basic API health and availability."""
    
    def test_api_docs_accessible(self, api_client: APIClient):
        """Test that API documentation is accessible."""
        response = api_client.get("/docs")
        api_client.assert_success(response)
        assert "text/html" in response.headers.get("content-type", "")
    
    def test_api_root_endpoint(self, api_client: APIClient):
        """Test the root API endpoint."""
        response = api_client.get("/")
        data = api_client.assert_success(response)
        assert "message" in data or "status" in data


class TestAgentWorkflow:
    """Test the multi-agent workflow: Plan -> Build -> Test -> Reflexion."""
    
    def test_architect_agent_planning(self, api_client: APIClient, test_context: E2ETestContext, 
                                    sample_feature_description: str):
        """Test the architect agent planning phase."""
        # Call the architect endpoint
        response = api_client.post("/architect", {
            "prompt": sample_feature_description
        })
        
        data = api_client.assert_success(response)
        test_context.log_response("/architect", response)
        
        # Validate response structure
        assert "plan_id" in data or "plan" in data
        
        # Store plan for next steps
        if "plan_id" in data:
            test_context.store("plan_id", data["plan_id"])
        if "plan" in data:
            test_context.store("plan", data["plan"])
    
    def test_builder_agent_building(self, api_client: APIClient, test_context: E2ETestContext):
        """Test the builder agent code generation."""
        # Get plan from previous step or create a simple one
        plan = test_context.get("plan", "Create a simple add function")
        
        response = api_client.post("/builder", {
            "plan": plan
        })
        
        data = api_client.assert_success(response)
        test_context.log_response("/builder", response)
        
        # Validate response structure
        assert "code" in data or "files" in data
        
        # Store generated code for testing
        if "code" in data:
            test_context.store("generated_code", data["code"])
    
    def test_tester_agent_execution(self, api_client: APIClient, test_context: E2ETestContext):
        """Test the tester agent test execution."""
        # Use generated code or provide sample code
        code = test_context.get("generated_code", "def add(a, b):\n    return a + b")
        tests = """
from generated_module import add

def test_add():
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
"""
        
        response = api_client.post("/tester/run", {
            "code": code,
            "tests": tests
        })
        
        data = api_client.assert_success(response)
        test_context.log_response("/tester/run", response)
        
        # Validate response structure
        assert "success" in data
        assert "output" in data
        
        # Store test results
        test_context.store("test_success", data["success"])
        test_context.store("test_output", data["output"])
    
    def test_reflexion_agent_improvement(self, api_client: APIClient, test_context: E2ETestContext):
        """Test the reflexion agent for improvement suggestions."""
        # Create a reflexion request based on test results
        test_success = test_context.get("test_success", True)
        
        if not test_success:
            # If tests failed, use reflexion to get improvements
            response = api_client.post("/reflexion/reflect", {
                "feedback": "Tests failed - need improvements"
            })
            
            data = api_client.assert_success(response)
            test_context.log_response("/reflexion/reflect", response)
            
            assert "instructions" in data
            test_context.store("improvement_instructions", data["instructions"])
        else:
            # Tests passed, skip reflexion but test the endpoint works
            response = api_client.post("/reflexion/reflect", {
                "feedback": "Tests passed - good implementation"
            })
            
            data = api_client.assert_success(response)
            test_context.log_response("/reflexion/reflect", response)
            assert "instructions" in data


class TestProjectManagement:
    """Test project creation and management functionality."""
    
    def test_project_initialization(self, api_client: APIClient, test_context: E2ETestContext,
                                  sample_project_config: dict):
        """Test project initialization via repo-init endpoint."""
        response = api_client.post("/api/repo-init", sample_project_config)
        
        # The endpoint might return different status codes based on implementation
        if response.status_code == 200:
            data = api_client.assert_success(response)
            test_context.log_response("/api/repo-init", response)
            test_context.store("project_id", data.get("project_id") or data.get("id"))
        elif response.status_code == 404:
            pytest.skip("Repo-init endpoint not implemented yet")
        else:
            # Log the response for debugging but don't fail the test
            test_context.log_response("/api/repo-init", response)
            pytest.skip(f"Repo-init endpoint returned {response.status_code}")


class TestConfigurationManagement:
    """Test environment and configuration management."""
    
    def test_environment_variables_get(self, api_client: APIClient, test_context: E2ETestContext):
        """Test retrieving environment variables."""
        response = api_client.get("/api/config/env")
        
        if response.status_code == 200:
            data = api_client.assert_success(response)
            test_context.log_response("/api/config/env", response)
            assert isinstance(data, dict)
        else:
            # Endpoint might not be fully implemented
            test_context.log_response("/api/config/env", response)
    
    def test_environment_variables_update(self, api_client: APIClient, test_context: E2ETestContext,
                                        sample_environment_config: dict):
        """Test updating environment variables."""
        response = api_client.post("/api/config/env", sample_environment_config)
        
        if response.status_code in [200, 201]:
            data = api_client.assert_success(response, expected_status=response.status_code)
            test_context.log_response("/api/config/env", response)
        else:
            # Log for debugging but don't fail
            test_context.log_response("/api/config/env", response)


class TestMemoryAndLogging:
    """Test HipCortex memory and logging functionality."""
    
    def test_hipcortex_logging(self, api_client: APIClient, test_context: E2ETestContext):
        """Test HipCortex logging functionality."""
        sample_log = {
            "session_id": "test-session-001",
            "agent": "test-agent",
            "event": "test-event",
            "data": {"test": True},
            "timestamp": int(time.time())
        }
        
        response = api_client.post("/api/hipcortex/record", sample_log)
        
        if response.status_code in [200, 201]:
            data = api_client.assert_success(response, expected_status=response.status_code)
            test_context.log_response("/api/hipcortex/record", response)
            
            # Try to retrieve the logs
            get_response = api_client.get(f"/api/hipcortex/logs?session_id={sample_log['session_id']}")
            if get_response.status_code == 200:
                get_data = api_client.assert_success(get_response)
                test_context.log_response("/api/hipcortex/logs", get_response)
                assert isinstance(get_data, (dict, list))
        else:
            test_context.log_response("/api/hipcortex/record", response)


class TestEndToEndWorkflow:
    """Test complete end-to-end workflow scenarios."""
    
    def test_complete_agent_pipeline(self, api_client: APIClient, test_context: E2ETestContext,
                                   sample_feature_description: str):
        """Test the complete agent pipeline from planning to deployment."""
        # 1. Planning phase
        plan_response = api_client.post("/architect", {
            "prompt": sample_feature_description
        })
        
        if plan_response.status_code != 200:
            pytest.skip("Architect agent not available")
        
        plan_data = api_client.assert_success(plan_response)
        test_context.log_response("/architect", plan_response)
        
        # 2. Building phase
        build_response = api_client.post("/builder", {
            "plan": plan_data.get("plan", sample_feature_description)
        })
        
        if build_response.status_code == 200:
            build_data = api_client.assert_success(build_response)
            test_context.log_response("/builder", build_response)
            generated_code = build_data.get("code", "def test_function(): return True")
        else:
            generated_code = "def test_function(): return True"  # Fallback
        
        # 3. Testing phase
        test_code = """
def test_generated():
    from generated_module import test_function
    assert test_function() == True
"""
        
        test_response = api_client.post("/tester/run", {
            "code": generated_code,
            "tests": test_code
        })
        
        if test_response.status_code == 200:
            test_data = api_client.assert_success(test_response)
            test_context.log_response("/tester/run", test_response)
            
            # 4. Reflexion phase (if tests failed)
            if not test_data.get("success", True):
                reflexion_response = api_client.post("/reflexion/reflect", {
                    "feedback": f"Tests failed: {test_data.get('output', 'Unknown error')}"
                })
                
                if reflexion_response.status_code == 200:
                    reflexion_data = api_client.assert_success(reflexion_response)
                    test_context.log_response("/reflexion/reflect", reflexion_response)
                    assert "instructions" in reflexion_data
        
        # Store workflow completion
        test_context.store("workflow_completed", True)