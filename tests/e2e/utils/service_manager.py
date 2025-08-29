"""Service manager for E2E tests - manages backend and frontend services."""

import subprocess
import time
import psutil
import requests
import signal
import os
from typing import Optional
from pathlib import Path


class ServiceManager:
    """Manages backend and frontend services for E2E testing."""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.backend_process: Optional[subprocess.Popen] = None
        self.frontend_process: Optional[subprocess.Popen] = None
        self.backend_port = 8000
        self.frontend_port = 3000
        
    def start_backend(self, timeout: int = 30) -> bool:
        """Start the FastAPI backend service."""
        try:
            # Start uvicorn from project root
            cmd = ["python", "-m", "uvicorn", "backend.main:app", "--port", str(self.backend_port)]
            env = os.environ.copy()
            env["PYTHONPATH"] = str(self.project_root)
            
            self.backend_process = subprocess.Popen(
                cmd,
                cwd=self.project_root,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid  # Create process group
            )
            
            # Wait for backend to be ready
            return self._wait_for_service(f"http://localhost:{self.backend_port}/docs", timeout)
            
        except Exception as e:
            print(f"Failed to start backend: {e}")
            return False
    
    def start_frontend(self, timeout: int = 60) -> bool:
        """Start the Next.js frontend service."""
        try:
            # Check if node_modules exists
            frontend_dir = self.project_root / "frontend"
            if not (frontend_dir / "node_modules").exists():
                print("Installing frontend dependencies...")
                subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
            
            # Start Next.js dev server
            cmd = ["npm", "run", "dev"]
            env = os.environ.copy()
            env["PORT"] = str(self.frontend_port)
            
            self.frontend_process = subprocess.Popen(
                cmd,
                cwd=frontend_dir,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid  # Create process group
            )
            
            # Wait for frontend to be ready
            return self._wait_for_service(f"http://localhost:{self.frontend_port}", timeout)
            
        except Exception as e:
            print(f"Failed to start frontend: {e}")
            return False
    
    def _wait_for_service(self, url: str, timeout: int) -> bool:
        """Wait for a service to become available."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code < 500:  # Accept any non-server-error response
                    print(f"Service ready at {url}")
                    return True
            except requests.exceptions.RequestException:
                pass
            
            time.sleep(2)
        
        print(f"Timeout waiting for service at {url}")
        return False
    
    def stop_all(self):
        """Stop both backend and frontend services."""
        self._stop_process(self.backend_process, "Backend")
        self._stop_process(self.frontend_process, "Frontend")
        
    def _stop_process(self, process: Optional[subprocess.Popen], name: str):
        """Stop a process and its children."""
        if not process:
            return
            
        try:
            # Kill the entire process group
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            
            # Wait for graceful shutdown
            try:
                process.wait(timeout=10)
                print(f"{name} stopped gracefully")
            except subprocess.TimeoutExpired:
                # Force kill if needed
                os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                process.wait()
                print(f"{name} force-killed")
                
        except (ProcessLookupError, OSError) as e:
            # Process might already be dead
            print(f"{name} process cleanup: {e}")
        finally:
            if process:
                process.stdout = None
                process.stderr = None
    
    def is_backend_running(self) -> bool:
        """Check if backend service is running."""
        try:
            response = requests.get(f"http://localhost:{self.backend_port}/docs", timeout=5)
            return response.status_code < 500
        except requests.exceptions.RequestException:
            return False
    
    def is_frontend_running(self) -> bool:
        """Check if frontend service is running.""" 
        try:
            response = requests.get(f"http://localhost:{self.frontend_port}", timeout=5)
            return response.status_code < 500
        except requests.exceptions.RequestException:
            return False
    
    def get_backend_url(self) -> str:
        """Get the backend service URL."""
        return f"http://localhost:{self.backend_port}"
        
    def get_frontend_url(self) -> str:
        """Get the frontend service URL."""
        return f"http://localhost:{self.frontend_port}"