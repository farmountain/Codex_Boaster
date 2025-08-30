# Filename suggestion: test_user_login.py

# Test: User Login
def test_user_login():
    from fastapi.testclient import TestClient
    from unittest.mock import patch

    from backend.main import app
    client = TestClient(app)

    # Mock the user login agent
    with patch("backend.auth.user_manager.login_user") as mock_login_user:
        # Simulate successful login
        mock_login_user.return_value = {
            "success": True,
            "session_id": "sess123",
            "dashboard_loaded": True
        }

        response = client.post("/auth/login", json={
            "email": "newuser@example.com",
            "password": "securepassword"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "session_id" in data
        assert data["dashboard_loaded"] is True

        # Simulate failed login attempts (block after 3)
        mock_login_user.return_value = {
            "success": False,
            "error": "Account locked after 3 failed attempts"
        }
        response = client.post("/auth/login", json={
            "email": "newuser@example.com",
            "password": "wrongpassword"
        })
        assert response.status_code == 403
        data = response.json()
        assert "error" in data
        assert "locked" in data["error"].lower() or "failed attempts" in data["error"].lower()