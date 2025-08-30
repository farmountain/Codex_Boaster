# Filename suggestion: test_feature_flag_configuration.py

# Test: Feature Flag Configuration
def test_feature_flag_configuration():
    from fastapi.testclient import TestClient
    from unittest.mock import patch

    from backend.main import app
    client = TestClient(app)

    # Mock the feature flag agent
    with patch("backend.config_agent.toggle_feature_flag") as mock_toggle_feature_flag:
        # Simulate successful feature flag toggle
        mock_toggle_feature_flag.return_value = {
            "success": True,
            "feature": "new_dashboard",
            "enabled": True
        }

        response = client.post("/config/feature_flag", json={
            "feature": "new_dashboard",
            "enabled": True
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["feature"] == "new_dashboard"
        assert data["enabled"] is True

        # Simulate error and revert toggle
        mock_toggle_feature_flag.return_value = {
            "success": False,
            "error": "Toggle failed",
            "reverted": True
        }
        response = client.post("/config/feature_flag", json={
            "feature": "new_dashboard",
            "enabled": False
        })
        assert response.status_code == 400
        data = response.json()
        assert data["reverted"] is True
        assert "error" in data