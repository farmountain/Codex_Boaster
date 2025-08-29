#!/bin/bash
# E2E Test Runner Script
# This script runs the complete end-to-end test suite for Codex Booster

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Codex Booster E2E Test Suite${NC}"
echo -e "${BLUE}========================================${NC}"

# Configuration
PROJECT_ROOT=$(dirname "$(readlink -f "$0")")/../
BACKEND_PORT=8000
FRONTEND_PORT=3000
TEST_TIMEOUT=300  # 5 minutes

# Cleanup function
cleanup() {
    echo -e "\n${YELLOW}Cleaning up services...${NC}"
    
    # Kill processes on our ports
    if command -v lsof >/dev/null 2>&1; then
        lsof -ti:$BACKEND_PORT | xargs -r kill -9 >/dev/null 2>&1 || true
        lsof -ti:$FRONTEND_PORT | xargs -r kill -9 >/dev/null 2>&1 || true
    fi
    
    # Kill by process pattern
    pkill -f "uvicorn.*backend.main" >/dev/null 2>&1 || true
    pkill -f "npm.*dev" >/dev/null 2>&1 || true
    pkill -f "next.*dev" >/dev/null 2>&1 || true
    
    echo -e "${GREEN}Cleanup completed${NC}"
}

# Setup cleanup trap
trap cleanup EXIT

# Check dependencies
echo -e "${BLUE}Checking dependencies...${NC}"

if ! command -v python >/dev/null 2>&1; then
    echo -e "${RED}Error: Python not found${NC}"
    exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
    echo -e "${RED}Error: npm not found${NC}"
    exit 1
fi

if ! python -c "import pytest" >/dev/null 2>&1; then
    echo -e "${RED}Error: pytest not installed${NC}"
    exit 1
fi

echo -e "${GREEN}Dependencies check passed${NC}"

# Install test dependencies
echo -e "${BLUE}Installing test dependencies...${NC}"
cd "$PROJECT_ROOT"

# Install Python E2E test dependencies
python -m pip install -q psutil requests || {
    echo -e "${RED}Failed to install Python dependencies${NC}"
    exit 1
}

echo -e "${GREEN}Dependencies installed${NC}"

# Parse command line arguments
RUN_UNIT_TESTS=true
RUN_E2E_TESTS=true
VERBOSE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --e2e-only)
            RUN_UNIT_TESTS=false
            shift
            ;;
        --unit-only)
            RUN_E2E_TESTS=false
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  --e2e-only    Run only E2E tests"
            echo "  --unit-only   Run only unit tests"
            echo "  --verbose     Verbose output"
            echo "  --help        Show this help"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

# Run unit tests first if requested
if [ "$RUN_UNIT_TESTS" = true ]; then
    echo -e "\n${BLUE}Running Unit Tests...${NC}"
    
    # Frontend unit tests
    echo -e "${BLUE}Running frontend unit tests...${NC}"
    cd frontend
    if [ "$VERBOSE" = true ]; then
        npm test
    else
        npm test --silent
    fi
    frontend_status=$?
    cd ..
    
    # Backend unit tests  
    echo -e "${BLUE}Running backend unit tests...${NC}"
    if [ "$VERBOSE" = true ]; then
        python -m pytest backend/tests --tb=short -v
    else
        python -m pytest backend/tests -q
    fi
    backend_status=$?
    
    if [ $frontend_status -ne 0 ] || [ $backend_status -ne 0 ]; then
        echo -e "${RED}Unit tests failed${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}Unit tests passed${NC}"
fi

# Run E2E tests if requested
if [ "$RUN_E2E_TESTS" = true ]; then
    echo -e "\n${BLUE}Running End-to-End Tests...${NC}"
    
    # Cleanup any existing services
    cleanup
    
    # Wait a moment for cleanup
    sleep 2
    
    # Set test environment variables
    export ENV=test
    export DEBUG=true
    export LOG_LEVEL=warning
    
    # Run E2E tests with pytest
    if [ "$VERBOSE" = true ]; then
        python -m pytest tests/e2e --tb=short -v -s
    else
        python -m pytest tests/e2e -q
    fi
    e2e_status=$?
    
    if [ $e2e_status -ne 0 ]; then
        echo -e "${RED}E2E tests failed${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}E2E tests passed${NC}"
fi

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}  All tests completed successfully!${NC}"
echo -e "${GREEN}========================================${NC}"

exit 0