# Codex Booster

Codex Booster is an AI‑native platform that turns natural language goals into
working software.  A set of specialised agents handle planning, code
generation, testing, reflexion and billing.  All reasoning state is recorded in
**HipCortex**, enabling a persistent memory of each build attempt.

### Key Features

- **Architect, Builder and Tester agents** follow a test-first workflow.
- **ReflexionAgent** refines instructions using the AUREUS framework.
- **Config, Repo‑Init and Deploy agents** automate environment setup and
  deployment.
- **Integration and Test‑Suite agents** connect external APIs and generate SIT
  / UAT flows.
- **Doc and Chat agents** create docs and expose reasoning traces in the
  dashboard.

- **Marketplace** lists MCP servers, LLM adapters and database connectors for easy integration


## Quickstart

### Backend

1. Install dependencies with `pip install -r requirements.txt`.
2. Run the API using `uvicorn backend.main:app --reload`.
3. Visit `/docs` for interactive API documentation.

### Frontend

1. `cd frontend`
2. Install dependencies via `npm install`.
3. Start the dev server using `npm run dev`.

## Tests

Execute Python tests with `pytest` and frontend tests with `npm test`.

To run all tests, including the UI components, execute:
```bash
pytest
npm test --silent
cd frontend && npm test --silent && cd ..
```

## Documentation

Architecture diagrams, design notes and the development roadmap are kept in
`docs/`. Start with [docs/README.md](docs/README.md) for an overview and see
[docs/usage.md](docs/usage.md) for a step-by-step usage guide. The

[Use Cases](docs/use_cases.md) page lists example prompts by value stream. See
[Marketplace Guide](docs/marketplace.md) if you want to contribute your own
connectors.

[Use Cases](docs/use_cases.md) page lists example prompts by value stream.

