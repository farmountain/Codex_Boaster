#!/usr/bin/env bash
set -euo pipefail

# Run unit tests with coverage threshold
npm test -- --coverage --coverageThreshold='{"global":{"branches":80,"functions":80,"lines":80,"statements":80}}'

# Lint the VS Code extension with no warnings allowed
npm --workspace vscodiam run lint -- --max-warnings=0

# Basic secrets scan using ripgrep for known secret patterns
# Ignores documentation and tests to minimise false positives
if rg -n '(sk_live|AKIA|AIzaSy)' --glob '!*.example*' --glob '!docs/**' --glob '!**/test*' --glob '!scripts/evaluate.sh' >/tmp/secret_scan.log; then
  echo "Potential secrets detected:" >&2
  cat /tmp/secret_scan.log >&2
  exit 1
fi

echo "Evaluation checks passed"
