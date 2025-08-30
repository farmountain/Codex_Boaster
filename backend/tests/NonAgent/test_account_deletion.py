# Filename suggestion: test_account_deletion.py

# Test: Account Deletion
def test_account_deletion():
    from fastapi.testclient import TestClient
    from unittest.mock import patch

    from backend.main import app
    client = TestClient(app)

    # Mock the account deletion agent
    with patch("backend.auth.delete_account") as mock_delete_account:
        # Simulate successful account deletion
        mock_delete_account.return_value = {
            "success": True,
            "account_removed": True,
            "data_wiped": True
        }

        response = client.post("/auth/delete_account", json={"user_id": "user123"})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["account_removed"] is True
        assert data["data_wiped"] is True

        # Simulate deletion failure
        mock_delete_account.return_value = {
            "success": False,
            "error": "Account deletion failed"
        }
        response = client.post("/auth/delete_account", json={"user_id": "user123"})
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert "fail" in data["error"].lower()