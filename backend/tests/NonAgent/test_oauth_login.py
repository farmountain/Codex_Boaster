# Filename suggestion: test_oauth_login.py

# Test: OAuth Login
def test_oauth_login():
    from fastapi.testclient import TestClient
    from unittest.mock import patch

    from backend.main import app
    client = TestClient(app)

    # Mock the OAuth login agent
    with patch("backend.auth.oauth_manager.login_with_google") as mock_login_with_google:
        # Simulate successful OAuth login
        mock_login_with_google.return_value = {
            "success": True,
            "session_id": "sess456",
            "dashboard_loaded": True
        }

        response = client.post("/auth/oauth/google", json={
            "token": "valid_google_token"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "session_id" in data
        assert data["dashboard_loaded"] is True

        # Simulate invalid token error
        mock_login_with_google.return_value = {
            "success": False,
            "error": "Invalid OAuth token"
        }
        response = client.post("/auth/oauth/google", json={
            "token": "invalid_token"
        })
        assert response.status_code == 401
        data = response.json()
        assert "error" in data
        assert "invalid" in data["error"].lower()