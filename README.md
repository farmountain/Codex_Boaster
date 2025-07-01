# Codex Booster

Codex Booster is an AI‑native platform that turns natural language goals into
working software.  A set of specialised agents handle planning, code
generation, testing, reflexion and billing.  All reasoning state is recorded in
**HipCortex**, enabling a persistent memory of each build attempt.

The current UI is organised around a sidebar project switcher, an **Agent
Panel** for chat-driven workflows and a modular workspace that lists active
repositories.  Users select language runtimes such as Python, Node or Rust
 and configure secrets directly in the browser.  Logs and agent confidence
 scores appear in the **Reflexion** panel so you can inspect every decision.
 The panel now lists a chronological history of each reflexion attempt with
 colour-coded confidence scores.

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

Additional UX highlights:

- **Multi-language runtime selection** allows Python, Node.js, Rust and more per project.
- **Modular workspaces** display repositories and tasks in real time.
- **Chat + Codex Agent interface** lets you refine instructions with chain-of-thought reasoning.


## Quickstart

### Backend

1. Install dependencies with `pip install -r requirements.txt`.
2. Run the API using `uvicorn backend.main:app --reload`.
3. Visit `/docs` for interactive API documentation.

### Frontend

1. `cd frontend`
2. Install dependencies via `npm install`.
3. Start the dev server using `npm run dev`.

### Terminal Runner

Run common setup commands directly from the dashboard.  Open the
**Configure Environment** page and use the embedded Terminal Runner to
execute commands such as `npm install` or `pytest`.  Logs are streamed
in real time and saved under `logs/runtime/` for later review.

### Runtime Configuration

Use the **Runtime Selector** and **EnvVarForm** components to choose your Python, Node or Rust versions and enter any required environment variables. Saving this form writes `.env`, `.env.template.json`, `docker-compose.yml` and `codexbooster.config.json` for repeatable setups.

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

