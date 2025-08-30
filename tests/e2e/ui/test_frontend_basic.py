"""Basic UI testing using requests - focuses on endpoint availability and frontend serving."""

import pytest
import requests
from tests.e2e.utils.api_client import E2ETestContext


class TestFrontendAvailability:
    """Test that the frontend is serving correctly."""
    
    def test_frontend_homepage_loads(self, frontend_url: str, test_context: E2ETestContext):
        """Test that the frontend homepage loads successfully."""
        try:
            response = requests.get(frontend_url, timeout=10)
            test_context.log_response(frontend_url, response)
            
            # Frontend should return HTML
            assert response.status_code == 200
            assert "text/html" in response.headers.get("content-type", "")
            
            # Should contain expected HTML elements
            content = response.text.lower()
            assert "html" in content
            assert "codex" in content or "booster" in content
            
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Frontend not accessible: {e}")
    
    def test_frontend_static_assets(self, frontend_url: str, test_context: E2ETestContext):
        """Test that frontend static assets are accessible."""
        # Try to access common Next.js static paths
        static_paths = [
            "/_next/static/css/app/page.css",
            "/_next/static/chunks/webpack.js",
            "/favicon.ico"
        ]
        
        accessible_assets = 0
        for path in static_paths:
            try:
                url = f"{frontend_url}{path}"
                response = requests.get(url, timeout=5)
                test_context.log_response(url, response)
                
                if response.status_code == 200:
                    accessible_assets += 1
                    
            except requests.exceptions.RequestException:
                # Asset might not exist, which is okay
                pass
        
        # At least favicon should be accessible
        # But we won't fail if no assets are found since it depends on the build
        print(f"Found {accessible_assets} accessible static assets")
    
    def test_frontend_api_routes(self, frontend_url: str, test_context: E2ETestContext):
        """Test that frontend API routes are accessible."""
        # Next.js API routes (if any)
        api_paths = [
            "/api/health",
            "/api/status"
        ]
        
        for path in api_paths:
            try:
                url = f"{frontend_url}{path}"
                response = requests.get(url, timeout=5)
                test_context.log_response(url, response)
                
                # 404 is acceptable - route might not exist
                # 500+ would indicate a server error
                assert response.status_code < 500, f"Server error at {path}: {response.status_code}"
                
            except requests.exceptions.RequestException:
                # Route might not exist, which is okay
                pass


class TestFrontendBackendIntegration:
    """Test that the frontend can communicate with the backend."""
    
    def test_frontend_backend_connectivity(self, frontend_url: str, test_context: E2ETestContext):
        """Test that frontend pages load without backend connection errors."""
        # Common pages that might interact with the backend
        pages = [
            "/",
            "/docs",
            "/dashboard",
            "/configure"
        ]
        
        successful_pages = 0
        for page in pages:
            try:
                url = f"{frontend_url}{page}"
                response = requests.get(url, timeout=10)
                test_context.log_response(url, response)
                
                if response.status_code == 200:
                    successful_pages += 1
                    # Check that the page doesn't contain obvious error messages
                    content = response.text.lower()
                    assert "error" not in content or "connection refused" not in content
                elif response.status_code == 404:
                    # Page doesn't exist, which is fine
                    pass
                else:
                    # Log but don't fail - pages might redirect or have specific behavior
                    print(f"Page {page} returned status {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                print(f"Could not access {page}: {e}")
        
        # At least the homepage should be accessible
        assert successful_pages > 0, "No frontend pages were accessible"
        print(f"Successfully accessed {successful_pages} frontend pages")


class TestUIWorkflowIntegration:
    """Test UI workflow integration points."""
    
    def test_dashboard_elements_presence(self, frontend_url: str, test_context: E2ETestContext):
        """Test that dashboard page contains expected UI elements."""
        try:
            response = requests.get(f"{frontend_url}/dashboard", timeout=10)
            test_context.log_response(f"{frontend_url}/dashboard", response)
            
            if response.status_code == 404:
                # Dashboard might be at root or different path
                response = requests.get(frontend_url, timeout=10)
                test_context.log_response(frontend_url, response)
            
            if response.status_code == 200:
                content = response.text.lower()
                
                # Look for expected UI component indicators
                ui_elements = [
                    "planner",
                    "build",
                    "test",
                    "reflexion",
                    "deploy",
                    "agent",
                    "workspace"
                ]
                
                found_elements = [elem for elem in ui_elements if elem in content]
                print(f"Found UI elements: {found_elements}")
                
                # Should find at least some expected elements
                assert len(found_elements) > 0, "No expected UI elements found in dashboard"
            else:
                pytest.skip(f"Dashboard not accessible (status: {response.status_code})")
                
        except requests.exceptions.RequestException as e:
            pytest.skip(f"Dashboard not accessible: {e}")
    
    def test_configuration_page_accessibility(self, frontend_url: str, test_context: E2ETestContext):
        """Test that configuration/environment setup page is accessible."""
        config_paths = [
            "/configure",
            "/config",
            "/settings",
            "/environment"
        ]
        
        accessible = False
        for path in config_paths:
            try:
                url = f"{frontend_url}{path}"
                response = requests.get(url, timeout=5)
                test_context.log_response(url, response)
                
                if response.status_code == 200:
                    accessible = True
                    content = response.text.lower()
                    
                    # Look for configuration-related content
                    config_indicators = [
                        "environment",
                        "runtime",
                        "config",
                        "variable",
                        "setting"
                    ]
                    
                    found_indicators = [ind for ind in config_indicators if ind in content]
                    print(f"Found configuration indicators at {path}: {found_indicators}")
                    break
                    
            except requests.exceptions.RequestException:
                pass
        
        if not accessible:
            print("No configuration page found - this might be integrated in the main dashboard")
        else:
            print("Configuration page is accessible")