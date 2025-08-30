# Filename suggestion: test_performance_benchmarking.py

# Test: Performance Benchmarking
def test_performance_benchmarking():
    from fastapi.testclient import TestClient
    from unittest.mock import patch

    from backend.main import app
    client = TestClient(app)

    # Mock the performance benchmarking agent
    with patch("backend.test_suite_agent.run_performance_benchmarks") as mock_run_benchmarks:
        # Simulate successful benchmark run
        mock_run_benchmarks.return_value = {
            "success": True,
            "metrics": {
                "response_time_ms": 120,
                "throughput_rps": 500
            },
            "meets_thresholds": True
        }

        response = client.post("/test_suite/run_benchmarks", json={"suite": "default"})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "metrics" in data
        assert data["meets_thresholds"] is True

        # Simulate resource overload (test stopped)
        mock_run_benchmarks.return_value = {
            "success": False,
            "error": "Resource overload detected",
            "test_stopped": True
        }
        response = client.post("/test_suite/run_benchmarks", json={"suite": "default"})
        assert response.status_code == 503
        data = response.json()
        assert data["test_stopped"] is True
        assert "error" in data