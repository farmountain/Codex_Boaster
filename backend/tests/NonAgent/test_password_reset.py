# Filename suggestion: test_password_reset.py

# Test: Password Reset
def test_password_reset():
    from fastapi.testclient import TestClient
    from unittest.mock import patch

    from backend.main import app
    client = TestClient(app)

    # Mock the password reset agent
    with patch("backend.auth.user_manager.reset_password") as mock_reset_password:
        # Simulate successful password reset
        mock_reset_password.return_value = {
            "success": True,
            "password_updated": True
        }

        response = client.post("/auth/reset_password", json={
            "email": "newuser@example.com",
            "token": "validtoken",
            "new_password": "newsecurepassword"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["password_updated"] is True

        # Simulate expired token error
        mock_reset_password.return_value = {
            "success": False,
            "error": "Token expired"
        }
        response = client.post("/auth/reset_password", json={
            "email": "newuser@example.com",
            "token": "expiredtoken",
            "new_password": "newsecurepassword"
        })
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert "expired" in data["error"].lower()