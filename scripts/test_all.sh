#!/bin/bash
# Main test runner - runs all tests including E2E
set -e

# Run unit tests
echo "Running unit tests..."
npm test --silent && pytest -q

# Check if E2E tests should run
if [ "$1" = "--with-e2e" ] || [ "$E2E_TESTS" = "true" ]; then
    echo "Running E2E tests..."
    ./scripts/test_e2e.sh --e2e-only
else
    echo "Skipping E2E tests (use --with-e2e flag or set E2E_TESTS=true to include)"
fi
