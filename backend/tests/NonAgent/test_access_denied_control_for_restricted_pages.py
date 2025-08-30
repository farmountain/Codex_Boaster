# Filename: test_access_control_for_restricted_pages.py
from fastapi.testclient import TestClient
from unittest.mock import patch
from backend.main import app
client = TestClient(app)

def test_access_denied_to_restricted_page():
    # A new mock is created for this test and will be properly torn down.
    with patch("backend.auth.access_manager.check_access") as mock_check_access:
        mock_check_access.return_value = {
            "access_granted": False,
            "redirect_url": "/login",
            "warning_logged": True
        }
        response = client.get("/restricted/page")
        assert response.status_code == 403
        data = response.json()
        assert data.get("access_granted") is False
        assert data.get("redirect_url") == "/login"
        assert data.get("warning_logged") is True