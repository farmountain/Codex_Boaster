# Filename suggestion: test_database_schema_setup.py

# Test: Database Schema Setup
def test_database_schema_setup():
    from fastapi.testclient import TestClient
    from unittest.mock import patch

    from backend.main import app
    client = TestClient(app)

    # Mock the database migration agent
    with patch("backend.database.init_db_schema") as mock_init_db_schema:
        # Simulate successful DB schema setup
        mock_init_db_schema.return_value = {
            "success": True,
            "tables": ["users", "posts"],
            "fields": {
                "users": ["id", "name", "email"],
                "posts": ["id", "user_id", "content"]
            },
            "constraints_applied": True
        }

        response = client.post("/database/init_schema")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "users" in data["tables"]
        assert "posts" in data["tables"]
        assert data["constraints_applied"] is True

        # Simulate migration failure and rollback
        mock_init_db_schema.return_value = {
            "success": False,
            "rollback": True,
            "error": "Migration failed"
        }
        response = client.post("/database/init_schema")
        assert response.status_code == 400
        data = response.json()
        assert data["rollback"] is True
        assert "error" in data