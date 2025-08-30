# Filename suggestion: test_api_key_generation.py

import pytest

# Test: API Key Generation
from fastapi.testclient import TestClient
from unittest.mock import patch
from backend.main import app

client = TestClient(app)

def test_api_key_generation_success():
    with patch("backend.auth.user_manager.generate_api_key") as mock_generate_api_key:
        mock_generate_api_key.return_value = {
            "success": True,
            "api_key": "abcdef123456"
        }
        response = client.post("/auth/generate_api_key", json={"user_id": "user123"})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "api_key" in data
        assert len(data["api_key"]) > 0

def test_api_key_generation_failure():
    test_client = TestClient(app, raise_server_exceptions=False)
    # Use a user_id that triggers the error branch in the real implementation
    response = test_client.post("/auth/generate_api_key", json={"user_id": "fail"})
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "fail" in data["detail"].lower()