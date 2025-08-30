# Filename suggestion: test_version_control_commit_push.py

# Test: Version Control Commit and Push
def test_version_control_commit_and_push():
    from fastapi.testclient import TestClient
    from unittest.mock import patch

    from backend.main import app
    client = TestClient(app)

    # Mock the version control agent
    with patch("backend.repo_init_agent.commit_and_push") as mock_commit_and_push:
        # Simulate successful commit and push
        mock_commit_and_push.return_value = {
            "success": True,
            "remote_url": "https://github.com/user/repo",
            "commit_hash": "abc123"
        }

        response = client.post("/repo_init/commit_push", json={
            "files": ["main.py", "utils.py"],
            "message": "Initial commit"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "remote_url" in data
        assert "commit_hash" in data

        # Simulate merge conflict (abort push)
        mock_commit_and_push.return_value = {
            "success": False,
            "error": "Merge conflict detected"
        }
        response = client.post("/repo_init/commit_push", json={
            "files": ["main.py"],
            "message": "Update main"
        })
        assert response.status_code == 409
        data = response.json()
        assert "error" in data
        assert "conflict" in data["error"].lower()