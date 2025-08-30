# Filename suggestion: test_load_testing.py

# Test: Load Testing
def test_load_testing():
    from fastapi.testclient import TestClient
    from unittest.mock import patch

    from backend.main import app
    client = TestClient(app)

    # Mock the load testing agent
    with patch("backend.test_suite_agent.run_load_test") as mock_run_load_test:
        # Simulate successful load test
        mock_run_load_test.return_value = {
            "success": True,
            "metrics": {
                "max_users": 1000,
                "avg_response_time_ms": 200,
                "error_rate": 0.01
            },
            "within_limits": True
        }

        response = client.post("/test_suite/run_load_test", json={"users": 1000, "duration": 60})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["within_limits"] is True
        assert "metrics" in data
        assert data["metrics"]["max_users"] == 1000

        # Simulate overload (test aborted)
        mock_run_load_test.return_value = {
            "success": False,
            "error": "System overload detected",
            "test_aborted": True
        }
        response = client.post("/test_suite/run_load_test", json={"users": 5000, "duration": 60})
        assert response.status_code == 503
        data = response.json()
        assert data["test_aborted"] is True
        assert "error" in data
        