import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from backend.main import app

client = TestClient(app)

# Filename suggestion: test_config_runtime.py
# Test: Environment Configuration and Runtime Selection
def test_environment_configuration_and_runtime_selection():
    with patch("backend.config_agent.update_config") as mock_update_config, \
         patch("backend.config_agent.select_runtime") as mock_select_runtime:
        mock_update_config.return_value = True
        mock_select_runtime.return_value = "python"

        response = client.post("/config/update", json={"API_KEY": "test", "DB_URL": "sqlite://"})
        assert response.status_code == 200
        assert response.json()["success"] is True

        response = client.post("/config/runtime", json={"runtime": "python"})
        assert response.status_code == 200
        assert response.json()["runtime"] == "python"

        mock_update_config.return_value = False
        response = client.post("/config/update", json={"API_KEY": ""})
        assert response.status_code == 400