# Filename suggestion: test_file_upload.py

# Test: File Upload
def test_file_upload():
    from fastapi.testclient import TestClient
    from unittest.mock import patch

    from backend.main import app
    client = TestClient(app)

    # Mock the file upload agent
    with patch("backend.services.file_service.upload_file") as mock_upload_file:
        # Simulate successful file upload
        mock_upload_file.return_value = {
            "success": True,
            "file_id": "abc123",
            "preview_url": "/preview/abc123"
        }

        response = client.post("/files/upload", files={"file": ("test.txt", b"Hello world")})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "file_id" in data
        assert "preview_url" in data

        # Simulate invalid file type rejection
        mock_upload_file.return_value = {
            "success": False,
            "error": "Invalid file type"
        }
        response = client.post("/files/upload", files={"file": ("malware.exe", b"binarydata")})
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert "invalid" in data["error"].lower()