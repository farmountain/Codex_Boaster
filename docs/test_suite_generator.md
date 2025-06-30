# Test Suite Generator

The **TestSuiteAgent** converts a high level business description into three artefacts:

- `unit_tests` – function level checks in pytest format
- `sit_tests` – system integration flows
- `uat_scenarios` – plain‑English acceptance criteria

Test templates live in `backend/test_suite_agent.py`. Modify or extend these snippets to match your preferred framework. The agent currently calls `generate_test_cases` from `backend.llm_client` which can be replaced with your own prompt logic.

To override templates:

1. Edit the default stubs under `generate_test_suite`.
2. Add any additional files or frameworks as needed.
3. Run the FastAPI server and POST to `/api/test-suite` to verify the output.
