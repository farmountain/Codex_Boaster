# Filename suggestion: test_data_import_from_csv.py

# Test: Data Import from CSV
def test_data_import_from_csv():
    from fastapi.testclient import TestClient
    from unittest.mock import patch

    from backend.main import app
    client = TestClient(app)

    # Mock the data import agent
    with patch("backend.database.import_csv") as mock_import_csv:
        # Simulate successful CSV import
        mock_import_csv.return_value = {
            "success": True,
            "imported_rows": 100,
            "errors": []
        }

        response = client.post("/database/import_csv", files={"file": ("data.csv", b"col1,col2\n1,2\n3,4")})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["imported_rows"] == 100
        assert data["errors"] == []

        # Simulate import with invalid rows (rollback)
        mock_import_csv.return_value = {
            "success": False,
            "rollback": True,
            "error": "Invalid rows detected",
            "invalid_rows": [2, 5, 8]
        }
        response = client.post("/database/import_csv", files={"file": ("data.csv", b"col1,col2\n1,2\nbad,row\n3,4")})
        assert response.status_code == 400
        data = response.json()
        assert data["rollback"] is True
        assert "error" in data
        assert "invalid_rows" in data