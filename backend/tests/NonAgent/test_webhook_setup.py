# Filename suggestion: test_webhook_setup.py

# Test: Webhook Setup
def test_webhook_setup():
    from fastapi.testclient import TestClient
    from unittest.mock import patch

    from backend.main import app
    client = TestClient(app)

    # Mock the webhook configuration agent
    with patch("backend.integrations.webhook_service.configure_webhook") as mock_configure_webhook:
        # Simulate successful webhook setup
        mock_configure_webhook.return_value = {
            "success": True,
            "webhook_url": "https://example.com/webhook",
            "triggered": True
        }

        response = client.post("/integrations/webhook", json={"url": "https://example.com/webhook"})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["webhook_url"] == "https://example.com/webhook"
        assert data["triggered"] is True

        # Simulate unreachable webhook (revert setup)
        mock_configure_webhook.return_value = {
            "success": False,
            "error": "Webhook unreachable",
            "reverted": True
        }
        response = client.post("/integrations/webhook", json={"url": "https://badurl.com/webhook"})
        assert response.status_code == 400
        data = response.json()
        assert data["reverted"] is True
        assert "error" in data
        assert "unreachable" in data["error"].lower()