# Filename suggestion: test_build_pipeline_execution.py

# Test: Build Pipeline Execution
def test_build_pipeline_execution():
    from fastapi.testclient import TestClient
    from unittest.mock import patch

    from backend.main import app
    client = TestClient(app)

    # Mock the build pipeline agent
    with patch("backend.repo_init_agent.run_build_pipeline") as mock_run_build_pipeline:
        # Simulate successful build
        mock_run_build_pipeline.return_value = {
            "success": True,
            "artifact": "dist/app.zip",
            "output": "Build completed successfully"
        }

        response = client.post("/repo_init/run_build")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "artifact" in data
        assert "output" in data
        assert "error" not in data

        # Simulate build failure (pipeline stops and logs)
        mock_run_build_pipeline.return_value = {
            "success": False,
            "error": "Build failed due to syntax error"
        }
        response = client.post("/repo_init/run_build")
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert "Build failed" in data["error"]