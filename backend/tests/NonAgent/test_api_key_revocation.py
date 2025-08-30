# Filename suggestion: test_api_key_revocation.py

# Test: API Key Revocation
def test_api_key_revocation():
    from fastapi.testclient import TestClient
    from unittest.mock import patch

    from backend.main import app
    client = TestClient(app)

    # Mock the API key revocation agent
    with patch("backend.auth.user_manager.revoke_api_key") as mock_revoke_api_key:
        # Simulate successful API key revocation
        mock_revoke_api_key.return_value = {
            "success": True,
            "key_invalidated": True
        }

        response = client.post("/auth/revoke_api_key", json={"user_id": "user123", "api_key": "abcdef123456"})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["key_invalidated"] is True

        # Simulate error if key not found
        mock_revoke_api_key.return_value = {
            "success": False,
            "error": "API key not found"
        }
        response = client.post("/auth/revoke_api_key", json={"user_id": "user123", "api_key": "notfoundkey"})
        assert response.status_code == 404
        data = response.json()
        assert "error" in data
        assert "not found" in data["error"].lower()