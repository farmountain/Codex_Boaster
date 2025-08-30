
# Filename suggestion: test_repo_init_cicd.py
# Test: Repository Initialization and CI/CD Setup
def test_repository_initialization_and_cicd_setup():
    with patch("backend.repo_init_agent.init_repo") as mock_init_repo:
        mock_init_repo.return_value = {
            "success": True,
            "repo_path": "/workspace/new_repo",
            "ci_files": [".github/workflows/main.yml"]
        }

        response = client.post("/repo_init", json={"template": "github-actions"})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "repo_path" in data
        assert ".github/workflows/main.yml" in data["ci_files"]

        mock_init_repo.return_value = {"success": False, "error": "Repo creation failed"}
        response = client.post("/repo_init", json={"template": "github-actions"})
        assert response.status_code == 400
        assert "error" in response.json()