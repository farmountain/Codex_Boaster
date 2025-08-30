# Filename suggestion: test_deployment_to_staging.py

# Test: Deployment to Staging
def test_deployment_to_staging():
    from fastapi.testclient import TestClient
    from unittest.mock import patch

    from backend.main import app
    client = TestClient(app)

    # Mock the deployment agent
    with patch("backend.deploy_agent.deploy_to_staging") as mock_deploy_to_staging:
        # Simulate successful deployment
        mock_deploy_to_staging.return_value = {
            "success": True,
            "staging_url": "https://staging.example.com",
            "health_check": "pass"
        }

        response = client.post("/deploy/staging")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "staging_url" in data
        assert data["health_check"] == "pass"

        # Simulate health check failure and automatic rollback
        mock_deploy_to_staging.return_value = {
            "success": False,
            "rollback": True,
            "error": "Health check failed"
        }
        response = client.post("/deploy/staging")
        assert response.status_code == 400
        data = response.json()
        assert data["rollback"] is True
        assert "error" in data