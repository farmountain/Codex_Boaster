# In your new test file, `test_access_granted_to_restricted_page.py`
from fastapi.testclient import TestClient
from unittest.mock import patch
from backend.main import app

client = TestClient(app, raise_server_exceptions=False)

# The rest of your test code follows below
def test_access_granted_to_restricted_page():
    with patch("backend.auth.access_manager.check_access") as mock_check_access:
        # Simulate access granted
        mock_check_access.return_value = {
            "access_granted": True
        }
        
        response = client.get("/restricted/page")
        assert response.status_code == 200
        data = response.json()
        assert data.get("access_granted") is True