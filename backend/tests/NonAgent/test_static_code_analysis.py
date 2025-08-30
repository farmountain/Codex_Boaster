# Filename suggestion: test_static_code_analysis.py

# Test: Static Code Analysis
def test_static_code_analysis():
    from fastapi.testclient import TestClient
    from unittest.mock import patch

    from backend.main import app
    client = TestClient(app)

    # Mock the static analysis agent
    with patch("backend.test_suite_agent.run_static_analysis") as mock_run_static_analysis:
        mock_run_static_analysis.return_value = {
            "success": True,
            "issues": [
                {"file": "main.py", "line": 10, "type": "warning", "message": "Unused import"},
                {"file": "utils.py", "line": 5, "type": "error", "message": "Undefined variable"}
            ]
        }

        response = client.post("/test_suite/run_static_analysis")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert any(issue["type"] == "warning" for issue in data["issues"])
        assert any(issue["type"] == "error" for issue in data["issues"])
        assert all("file" in issue and "line" in issue for issue in data["issues"])

        # Simulate critical issue detected (block commit)
        mock_run_static_analysis.return_value = {
            "success": False,
            "block_commit": True,
            "issues": [
                {"file": "core.py", "line": 42, "type": "error", "message": "Security vulnerability"}
            ]
        }
        response = client.post("/test_suite/run_static_analysis")
        assert response.status_code == 400
        data = response.json()
        assert data["block_commit"] is True
        assert any(issue["type"] == "error" for issue in data["issues"])