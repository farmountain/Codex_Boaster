# Filename suggestion: test_log_retention_policy_update.py

# Test: Log Retention Policy Update
def test_log_retention_policy_update():
    from fastapi.testclient import TestClient
    from unittest.mock import patch

    from backend.main import app
    client = TestClient(app)

    # Mock the log retention policy agent
    with patch("backend.logging.log_manager.update_retention_policy") as mock_update_retention_policy:
        # Simulate successful policy update
        mock_update_retention_policy.return_value = {
            "success": True,
            "retention_days": 30,
            "policy_applied": True
        }

        response = client.post("/logging/update_retention", json={"days": 30})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["retention_days"] == 30
        assert data["policy_applied"] is True

        # Simulate invalid period (revert)
        mock_update_retention_policy.return_value = {
            "success": False,
            "error": "Invalid retention period",
            "reverted": True
        }
        response = client.post("/logging/update_retention", json={"days": -5})
        assert response.status_code == 400
        data = response.json()
        assert data["reverted"] is True
        assert "error" in data
        assert "invalid" in data["error"].lower()