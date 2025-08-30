"""Pytest configuration and fixtures for E2E tests."""

import pytest
import tempfile
import shutil
from pathlib import Path
from typing import Generator

from tests.e2e.utils.service_manager import ServiceManager
from tests.e2e.utils.api_client import APIClient, E2ETestContext


@pytest.fixture(scope="session")
def project_root() -> str:
    """Get the project root directory."""
    return str(Path(__file__).parent.parent.parent)


@pytest.fixture(scope="session")
def service_manager(project_root: str) -> Generator[ServiceManager, None, None]:
    """Manage backend and frontend services for the test session."""
    manager = ServiceManager(project_root)
    
    # Start services
    print("\nStarting E2E test services...")
    
    backend_started = manager.start_backend(timeout=30)
    if not backend_started:
        pytest.skip("Could not start backend service")
    
    frontend_started = manager.start_frontend(timeout=60)
    if not frontend_started:
        pytest.skip("Could not start frontend service")
    
    print("All services started successfully")
    
    yield manager
    
    # Cleanup
    print("\nStopping E2E test services...")
    manager.stop_all()


@pytest.fixture
def api_client(service_manager: ServiceManager) -> APIClient:
    """API client for making requests to the backend."""
    return APIClient(service_manager.get_backend_url())


@pytest.fixture
def frontend_url(service_manager: ServiceManager) -> str:
    """Get the frontend URL."""
    return service_manager.get_frontend_url()


@pytest.fixture
def test_context() -> Generator[E2ETestContext, None, None]:
    """Test context for storing data and artifacts."""
    context = E2ETestContext()
    yield context
    
    # Cleanup artifacts if needed
    for artifact in context.test_artifacts:
        artifact_path = Path(artifact['path'])
        if artifact_path.exists():
            if artifact_path.is_dir():
                shutil.rmtree(artifact_path)
            else:
                artifact_path.unlink()


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


# Test data fixtures
@pytest.fixture
def sample_project_config() -> dict:
    """Sample project configuration for testing."""
    return {
        "name": "test-project",
        "description": "Test project for E2E validation",
        "runtime": "python",
        "version": "3.12",
        "repository_url": "https://github.com/test-org/test-project",
        "setup_script": "pip install -r requirements.txt"
    }


@pytest.fixture
def sample_feature_description() -> str:
    """Sample feature description for agent testing."""
    return """
    Create a simple calculator function that can perform basic arithmetic operations:
    - Addition of two numbers
    - Subtraction of two numbers  
    - Multiplication of two numbers
    - Division of two numbers (with zero division handling)
    
    The function should return appropriate error messages for invalid operations.
    """


@pytest.fixture
def sample_environment_config() -> dict:
    """Sample environment configuration."""
    return {
        "python_version": "3.12",
        "node_version": "18",
        "environment_variables": {
            "ENV": "test",
            "DEBUG": "true",
            "LOG_LEVEL": "debug"
        }
    }