"""API client utilities for E2E testing."""

import requests
from typing import Dict, Any, Optional
import json


class APIClient:
    """HTTP client for testing API endpoints."""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'E2E-Test-Client/1.0'
        })
    
    def get(self, endpoint: str, **kwargs) -> requests.Response:
        """Make GET request to API endpoint."""
        url = f"{self.base_url}{endpoint}"
        return self.session.get(url, **kwargs)
    
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """Make POST request to API endpoint."""
        url = f"{self.base_url}{endpoint}"
        if data:
            kwargs['json'] = data
        return self.session.post(url, **kwargs)
    
    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """Make PUT request to API endpoint."""
        url = f"{self.base_url}{endpoint}"
        if data:
            kwargs['json'] = data
        return self.session.put(url, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """Make DELETE request to API endpoint."""
        url = f"{self.base_url}{endpoint}"
        return self.session.delete(url, **kwargs)
    
    def health_check(self) -> bool:
        """Check if API is healthy."""
        try:
            response = self.get("/docs")
            return response.status_code < 500
        except requests.exceptions.RequestException:
            return False
    
    def assert_success(self, response: requests.Response, expected_status: int = 200) -> Dict[str, Any]:
        """Assert response is successful and return JSON data."""
        assert response.status_code == expected_status, \
            f"Expected {expected_status}, got {response.status_code}: {response.text}"
        
        if response.headers.get('content-type', '').startswith('application/json'):
            return response.json()
        return {}
    
    def assert_error(self, response: requests.Response, expected_status: int) -> Dict[str, Any]:
        """Assert response is an expected error and return JSON data."""
        assert response.status_code == expected_status, \
            f"Expected {expected_status}, got {response.status_code}: {response.text}"
        
        if response.headers.get('content-type', '').startswith('application/json'):
            return response.json()
        return {}


class E2ETestContext:
    """Context manager for E2E test data and state."""
    
    def __init__(self):
        self.data = {}
        self.api_responses = []
        self.test_artifacts = []
    
    def store(self, key: str, value: Any):
        """Store test data."""
        self.data[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve test data."""
        return self.data.get(key, default)
    
    def log_response(self, endpoint: str, response: requests.Response):
        """Log API response for debugging."""
        self.api_responses.append({
            'endpoint': endpoint,
            'status_code': response.status_code,
            'response_time': response.elapsed.total_seconds(),
            'headers': dict(response.headers),
            'body': response.text[:1000] if response.text else None  # Truncate large responses
        })
    
    def add_artifact(self, name: str, path: str):
        """Track test artifacts for cleanup."""
        self.test_artifacts.append({'name': name, 'path': path})
    
    def get_summary(self) -> Dict[str, Any]:
        """Get test execution summary."""
        return {
            'data_items': len(self.data),
            'api_calls': len(self.api_responses),
            'artifacts': len(self.test_artifacts),
            'failed_responses': len([r for r in self.api_responses if r['status_code'] >= 400])
        }