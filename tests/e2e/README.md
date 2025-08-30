# End-to-End Test Suite

This directory contains the complete end-to-end (E2E) test suite for Codex Booster. The tests validate the entire user journey as described in `docs/e2e_test_plan.md`, from installation to deployment.

## Structure

```
tests/e2e/
├── api/                      # API endpoint tests
│   └── test_core_functionality.py
├── ui/                       # Frontend UI tests
│   └── test_frontend_basic.py  
├── utils/                    # Test utilities and helpers
│   ├── __init__.py
│   ├── api_client.py         # HTTP client for API testing
│   └── service_manager.py    # Service orchestration (start/stop backend/frontend)
├── fixtures/                 # Test data and fixtures (future use)
├── conftest.py              # Pytest configuration and fixtures
├── test_complete_workflow.py # Complete workflow tests
└── README.md                # This file
```

## Features

### Service Orchestration
- **Automatic service management**: Tests automatically start and stop backend (FastAPI) and frontend (Next.js) services
- **Health checking**: Waits for services to be ready before running tests
- **Port management**: Uses configurable ports (8000 for backend, 3000 for frontend)
- **Cleanup**: Automatically cleans up services after tests complete

### Test Categories

1. **API Health Tests**: Verify basic API availability and health
2. **Agent Workflow Tests**: Test the complete multi-agent workflow (Plan → Build → Test → Reflexion → Deploy)
3. **Frontend Availability Tests**: Verify frontend is serving correctly and accessible
4. **Integration Tests**: Test frontend-backend communication
5. **Complete User Journey Tests**: End-to-end validation of the full user experience

### Test Context Management
- **State tracking**: Tests can store and retrieve data across test phases
- **Response logging**: All API responses are logged for debugging
- **Artifact management**: Automatic cleanup of test artifacts

## Running Tests

### Using the E2E Test Runner
```bash
# Run all tests (unit + E2E)
./scripts/test_e2e.sh

# Run only E2E tests
./scripts/test_e2e.sh --e2e-only

# Run only unit tests  
./scripts/test_e2e.sh --unit-only

# Run with verbose output
./scripts/test_e2e.sh --verbose
```

### Using pytest directly
```bash
# Run all E2E tests
python -m pytest tests/e2e

# Run specific test file
python -m pytest tests/e2e/api/test_core_functionality.py

# Run specific test
python -m pytest tests/e2e/api/test_core_functionality.py::TestAPIHealthCheck::test_api_docs_accessible

# Run with verbose output
python -m pytest tests/e2e -v -s
```

### Using the main test script
```bash
# Run unit tests only (default)
./scripts/test_all.sh

# Include E2E tests
./scripts/test_all.sh --with-e2e

# Or set environment variable
E2E_TESTS=true ./scripts/test_all.sh
```

## Test Scenarios

### Installation & Setup
- ✅ Backend API availability (uvicorn/FastAPI)
- ✅ Frontend dev server (React/Next.js)
- ✅ Service health checks

### Configuration Workflow
- ✅ Environment configuration retrieval
- ✅ Runtime selector functionality
- ✅ Environment variable updates

### Project Creation
- ✅ Project initialization via repo-init
- ✅ Project metadata validation

### Agent Interactions Workflow
- ✅ **Planning Phase**: Architect agent planning (`POST /architect`)
- ✅ **Building Phase**: Builder agent code generation (`POST /builder`)
- ✅ **Testing Phase**: Tester agent test execution (`POST /tester/run`)
- ✅ **Reflexion Phase**: Reflexion agent improvements (`POST /reflexion`)
- ✅ **Deployment Phase**: Deploy agent deployment (`POST /api/deploy`)

### UI Integration
- ✅ Frontend homepage accessibility
- ✅ Static asset serving
- ✅ Dashboard elements presence
- ✅ Configuration page accessibility

### Memory & Logging
- ✅ HipCortex logging functionality
- ✅ Session management
- ✅ Memory snapshot retrieval

## Configuration

Tests use the following default configuration:
- Backend port: `8000`
- Frontend port: `3000`
- Service startup timeout: `30s` (backend), `60s` (frontend)
- Test timeout: `300s` (5 minutes)

Configuration can be customized via environment variables:
```bash
export BACKEND_PORT=8001
export FRONTEND_PORT=3001
export TEST_TIMEOUT=600
```

## Dependencies

The E2E test suite requires:
- Python packages: `pytest`, `requests`, `psutil`
- Node.js and npm (for frontend)
- All project dependencies installed

Dependencies are automatically installed by the test runner script.

## Debugging

### Test Logs
Each test logs API responses and service interactions. Enable verbose mode to see detailed output:
```bash
python -m pytest tests/e2e -v -s --tb=short
```

### Service Debugging
If services fail to start:
1. Check port availability: `lsof -i :8000` and `lsof -i :3000`
2. Check service logs in the test output
3. Run services manually to debug issues:
   ```bash
   # Start backend
   python -m uvicorn backend.main:app --reload
   
   # Start frontend  
   cd frontend && npm run dev
   ```

### Common Issues
- **Port conflicts**: Change ports if 8000/3000 are in use
- **Service startup timeout**: Increase timeout for slower systems
- **Module import errors**: Ensure PYTHONPATH includes project root
- **Frontend build issues**: Run `npm install` in frontend directory

## Extending Tests

### Adding New Test Cases
1. Create test files in appropriate subdirectories (`api/`, `ui/`)
2. Use existing fixtures from `conftest.py`
3. Follow naming convention: `test_*.py`
4. Use test context for state management between test phases

### Adding New Fixtures
Add new fixtures to `conftest.py` or create fixture files in `fixtures/` directory.

### Adding New Utilities
Add utility functions to `utils/` directory and import in test files.

## CI/CD Integration

The E2E test suite is designed to work in CI/CD environments:
- Headless operation (no browser dependencies for basic tests)
- Configurable timeouts
- Proper service cleanup
- Exit codes for build systems
- Environment variable configuration

For GitHub Actions, Azure DevOps, or other CI systems, use:
```yaml
- name: Run E2E Tests
  run: ./scripts/test_e2e.sh
  env:
    E2E_TESTS: true
```