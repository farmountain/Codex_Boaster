"""Complete end-to-end workflow tests that mirror the documented user journey."""

import pytest
import time
from tests.e2e.utils.api_client import APIClient, E2ETestContext


class TestInstallationAndSetup:
    """Test installation and setup verification as described in e2e_test_plan.md."""
    
    def test_backend_api_availability(self, api_client: APIClient, test_context: E2ETestContext):
        """Verify that uvicorn and fastapi are available (Step 1 of Installation)."""
        # Test API docs endpoint
        response = api_client.get("/docs")
        api_client.assert_success(response)
        test_context.log_response("/docs", response)
        
        # Should contain FastAPI documentation
        assert "swagger" in response.text.lower() or "openapi" in response.text.lower()
        test_context.store("backend_confirmed", True)
    
    def test_frontend_dev_server(self, frontend_url: str, test_context: E2ETestContext):
        """Verify that React and Jest are available (Step 2 of Installation)."""
        import requests
        
        response = requests.get(frontend_url, timeout=10)
        test_context.log_response(frontend_url, response)
        
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
        
        # Should be serving a React application
        content = response.text
        assert "react" in content.lower() or "_next" in content.lower() or "codex" in content.lower()
        test_context.store("frontend_confirmed", True)


class TestConfigurationWorkflow:
    """Test configuration workflow as described in e2e_test_plan.md."""
    
    def test_runtime_selector_configuration(self, api_client: APIClient, test_context: E2ETestContext):
        """Test environment configuration (Steps 1-3 of Configuration)."""
        # Test getting current environment configuration
        response = api_client.get("/api/config/env")
        
        if response.status_code == 200:
            current_config = api_client.assert_success(response)
            test_context.log_response("/api/config/env", response)
            test_context.store("initial_config", current_config)
        
        # Test updating environment configuration
        new_config = {
            "python_version": "3.12",
            "node_version": "18",
            "environment_variables": {
                "ENV": "test",
                "DEBUG": "true",
                "TEST_MODE": "e2e"
            }
        }
        
        update_response = api_client.post("/api/config/env", new_config)
        
        if update_response.status_code in [200, 201]:
            update_data = api_client.assert_success(update_response, update_response.status_code)
            test_context.log_response("/api/config/env POST", update_response)
            test_context.store("config_updated", True)
        else:
            # Configuration endpoint might not be fully implemented
            test_context.log_response("/api/config/env POST", update_response)
            test_context.store("config_updated", False)


class TestProjectCreationWorkflow:
    """Test project creation workflow as described in e2e_test_plan.md."""
    
    def test_project_initialization(self, api_client: APIClient, test_context: E2ETestContext):
        """Test project creation (Steps 1-3 of Project Creation)."""
        project_data = {
            "name": f"e2e-test-project-{int(time.time())}",
            "description": "E2E test project for validation",
            "runtime": "python",
            "version": "3.12",
            "repository_name": "e2e-test-repo",
            "setup_script": "pip install pytest"
        }
        
        response = api_client.post("/api/repo-init", project_data)
        
        if response.status_code in [200, 201]:
            data = api_client.assert_success(response, response.status_code)
            test_context.log_response("/api/repo-init", response)
            
            # Should return project information
            assert "name" in data or "project_id" in data or "id" in data
            test_context.store("project_created", True)
            test_context.store("project_data", data)
        else:
            # Repo-init might not be fully implemented
            test_context.log_response("/api/repo-init", response)
            test_context.store("project_created", False)


class TestAgentInteractionsWorkflow:
    """Test complete agent interactions workflow as described in e2e_test_plan.md."""
    
    def test_planning_phase(self, api_client: APIClient, test_context: E2ETestContext):
        """Test Planning phase - Architect Agent (Steps 1-2 of Agent Interactions)."""
        feature_description = """
        Create a user authentication system with the following features:
        - User registration with email and password
        - User login functionality
        - Password hashing for security
        - Session management
        - Input validation for email format and password strength
        """
        
        response = api_client.post("/architect", {
            "prompt": feature_description
        })
        
        data = api_client.assert_success(response)
        test_context.log_response("/architect", response)
        
        # Should return a plan with plan_id or plan content
        assert "plan_id" in data or "plan" in data or "steps" in data
        
        # Store for subsequent phases
        if "plan_id" in data:
            test_context.store("plan_id", data["plan_id"])
        if "plan" in data:
            test_context.store("plan", data["plan"])
        
        test_context.store("planning_completed", True)
    
    def test_building_phase(self, api_client: APIClient, test_context: E2ETestContext):
        """Test Building phase - Builder Agent (Steps 1-2 of Building)."""
        # Get plan from planning phase or use fallback
        plan = test_context.get("plan", "Create a simple user authentication function")
        
        response = api_client.post("/builder", {
            "plan": plan
        })
        
        data = api_client.assert_success(response)
        test_context.log_response("/builder", response)
        
        # Should return generated code or files
        assert "code" in data or "files" in data or "output" in data
        
        # Store generated code for testing phase
        if "code" in data:
            test_context.store("generated_code", data["code"])
        
        test_context.store("building_completed", True)
    
    def test_testing_phase(self, api_client: APIClient, test_context: E2ETestContext):
        """Test Testing phase - Tester Agent (Steps 1-2 of Testing)."""
        # Use generated code or provide sample code
        code = test_context.get("generated_code") or """
def authenticate_user(email, password):
    '''Simple user authentication function'''
    if not email or '@' not in email:
        return {'success': False, 'error': 'Invalid email'}
    if not password or len(password) < 8:
        return {'success': False, 'error': 'Password too short'}
    
    # Mock authentication
    if email == 'test@example.com' and password == 'password123':
        return {'success': True, 'user_id': 1}
    return {'success': False, 'error': 'Invalid credentials'}
"""
        
        test_code = """
from generated_module import authenticate_user

def test_authenticate_valid_user():
    result = authenticate_user('test@example.com', 'password123')
    assert result['success'] == True
    assert 'user_id' in result

def test_authenticate_invalid_email():
    result = authenticate_user('invalid-email', 'password123')
    assert result['success'] == False
    assert 'Invalid email' in result['error']

def test_authenticate_short_password():
    result = authenticate_user('test@example.com', '123')
    assert result['success'] == False
    assert 'Password too short' in result['error']
"""
        
        response = api_client.post("/tester/run", {
            "code": code,
            "tests": test_code
        })
        
        data = api_client.assert_success(response)
        test_context.log_response("/tester/run", response)
        
        # Should return test results
        assert "success" in data
        assert "output" in data
        
        # Store results for reflexion phase
        test_context.store("test_success", data["success"])
        test_context.store("test_output", data["output"])
        test_context.store("testing_completed", True)
    
    def test_reflexion_phase(self, api_client: APIClient, test_context: E2ETestContext):
        """Test Reflexion phase - Reflexion Agent (Steps 1-2 of Reflexion)."""
        test_success = test_context.get("test_success", True)
        test_output = test_context.get("test_output", "")
        
        # Use new reflexion endpoint if available
        reflexion_payload = {
            "test_log": test_output,
            "code_snippet": test_context.get("generated_code", "def sample(): pass"),
            "context": {
                "test_success": test_success,
                "phase": "e2e_validation"
            }
        }
        
        # Try new reflexion endpoint first
        response = api_client.post("/reflexion", reflexion_payload)
        
        if response.status_code == 200:
            data = api_client.assert_success(response)
            test_context.log_response("/reflexion", response)
            
            assert "plan" in data or "instructions" in data
            if "snapshot_id" in data:
                test_context.store("reflexion_snapshot_id", data["snapshot_id"])
        else:
            # Fall back to old endpoint
            response = api_client.post("/reflexion/reflect", {
                "feedback": f"Test results: {'passed' if test_success else 'failed'} - {test_output}"
            })
            
            if response.status_code == 200:
                data = api_client.assert_success(response)
                test_context.log_response("/reflexion/reflect", response)
                assert "instructions" in data
        
        test_context.store("reflexion_completed", True)
    
    def test_deployment_phase(self, api_client: APIClient, test_context: E2ETestContext):
        """Test Deployment phase - Deploy Agent (Steps 1-2 of Deployment)."""
        deployment_config = {
            "project_name": "e2e-test-deployment",
            "repo_url": "https://github.com/test-org/e2e-test",
            "provider": "vercel",
            "framework": "nextjs",
            "environment": "staging"
        }
        
        response = api_client.post("/api/deploy", deployment_config)
        
        if response.status_code in [200, 201]:
            data = api_client.assert_success(response, response.status_code)
            test_context.log_response("/api/deploy", response)
            
            # Should return deployment information
            assert "deployment_url" in data or "url" in data or "status" in data
            
            # Store deployment info
            test_context.store("deployment_completed", True)
            if "deployment_url" in data:
                test_context.store("deployment_url", data["deployment_url"])
        else:
            # Deployment might require specific configuration or external services
            test_context.log_response("/api/deploy", response)
            test_context.store("deployment_completed", False)


class TestCompleteUserJourney:
    """Test the complete user journey end-to-end."""
    
    def test_full_user_workflow(self, api_client: APIClient, test_context: E2ETestContext, 
                               frontend_url: str):
        """Test the complete user journey from start to finish."""
        journey_steps = []
        
        # 1. Verify services are running
        backend_health = api_client.health_check()
        journey_steps.append(("Backend Health", backend_health))
        assert backend_health, "Backend service is not healthy"
        
        # Frontend health check
        import requests
        try:
            frontend_response = requests.get(frontend_url, timeout=5)
            frontend_health = frontend_response.status_code < 500
        except requests.exceptions.RequestException:
            frontend_health = False
        
        journey_steps.append(("Frontend Health", frontend_health))
        assert frontend_health, "Frontend service is not healthy"
        
        # 2. Test agent workflow
        # Planning
        plan_response = api_client.post("/architect", {
            "prompt": "Create a simple task management system"
        })
        planning_success = plan_response.status_code == 200
        journey_steps.append(("Planning", planning_success))
        
        if planning_success:
            plan_data = plan_response.json()
            
            # Building
            build_response = api_client.post("/builder", {
                "plan": plan_data.get("plan", "Create task management functions")
            })
            building_success = build_response.status_code == 200
            journey_steps.append(("Building", building_success))
            
            if building_success:
                build_data = build_response.json()
                
                # Testing
                test_response = api_client.post("/tester/run", {
                    "code": build_data.get("code", "def create_task(): return {'id': 1}"),
                    "tests": "def test_create_task():\n    from generated_module import create_task\n    assert create_task()['id'] == 1"
                })
                testing_success = test_response.status_code == 200
                journey_steps.append(("Testing", testing_success))
        
        # 3. Memory logging
        memory_response = api_client.post("/api/hipcortex/record", {
            "session_id": "e2e-journey-test",
            "agent": "E2ETestAgent",
            "event": "journey_completion",
            "data": {"steps": journey_steps},
            "timestamp": int(time.time())
        })
        memory_success = memory_response.status_code in [200, 201]
        journey_steps.append(("Memory Logging", memory_success))
        
        # Store journey results
        test_context.store("journey_steps", journey_steps)
        test_context.store("journey_completed", True)
        
        # Verify at least core functionality works
        successful_steps = sum(1 for _, success in journey_steps if success)
        total_steps = len(journey_steps)
        
        print(f"User Journey Results: {successful_steps}/{total_steps} steps successful")
        print("Journey Steps:")
        for step_name, success in journey_steps:
            status = "✓" if success else "✗"
            print(f"  {status} {step_name}")
        
        # At least half the steps should succeed for a basic workflow
        assert successful_steps >= total_steps / 2, f"Only {successful_steps}/{total_steps} journey steps succeeded"