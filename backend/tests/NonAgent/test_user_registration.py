# Filename suggestion: test_user_registration.py

# Test: User Registration
def test_user_registration():
    from fastapi.testclient import TestClient
    from unittest.mock import patch

    from backend.main import app
    client = TestClient(app)

    # Mock the user registration agent
    with patch("backend.auth.user_manager.register_user") as mock_register_user:
        # Simulate successful registration
        mock_register_user.return_value = {
            "success": True,
            "user_id": "user123",
            "welcome_email_sent": True
        }

        response = client.post("/auth/register", json={
            "email": "newuser@example.com",
            "password": "securepassword",
            "name": "New User"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert "user_id" in data
        assert data["welcome_email_sent"] is True

        # Simulate duplicate email error
        mock_register_user.return_value = {
            "success": False,
            "error": "Email already exists"
        }
        response = client.post("/auth/register", json={
            "email": "newuser@example.com",
            "password": "securepassword",
            "name": "New User"
        })
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert "duplicate" in data["error"].lower() or "exists" in data["error"].lower()