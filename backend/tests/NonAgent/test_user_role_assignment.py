# Filename suggestion: test_user_role_assignment.py

# Test: User Role Assignment
def test_user_role_assignment():
    from fastapi.testclient import TestClient
    from unittest.mock import patch

    from backend.main import app
    client = TestClient(app)

    # Mock the user management agent
    with patch("backend.auth.user_manager.assign_role") as mock_assign_role:
        # Simulate successful role assignment
        mock_assign_role.return_value = {
            "success": True,
            "user_id": "user123",
            "role": "admin"
        }

        response = client.post("/auth/assign_role", json={
            "user_id": "user123",
            "role": "admin"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["role"] == "admin"

        # Simulate invalid role (prevent save)
        mock_assign_role.return_value = {
            "success": False,
            "error": "Invalid role"
        }
        response = client.post("/auth/assign_role", json={
            "user_id": "user123",
            "role": "superuser"
        })
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert "invalid" in data["error"].lower()