# Codex Booster

Codex Booster is an AI‑native platform that turns natural language goals into
working software.  A set of specialised agents handle planning, code
generation, testing, reflexion and billing.  All reasoning state is recorded in
**HipCortex**, enabling a persistent memory of each build attempt.

The project implements a multi-agent workflow based on the best practices in the [Codex Booster Agentic Framework](docs/agentic-framework.md). Planning starts with Parahelp SOP prompts, build tasks use prompt folding, testing relies on debug logs and reflexion chains and an orchestrator manages deployments and prompt library updates.

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
- **Hugging Face Transformers** library enables offline code generation

Additional UX highlights:

- **Multi-language runtime selection** allows Python, Node.js, Rust and more per project.
- **Modular workspaces** display repositories and tasks in real time.
- **Chat + Codex Agent interface** lets you refine instructions with chain-of-thought reasoning.


## Quickstart

### Backend

1. Install dependencies with `pip install -r requirements.txt`.
2. From the project root, run the API using `uvicorn backend.main:app --reload`.
   Running the command elsewhere can lead to `ModuleNotFoundError` for the
   `backend` package.
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

Use the **Runtime Selector** and **EnvVarForm** components to choose your Python, Node.js, Ruby, Rust, Go, Bun, Java or Swift versions and manage secrets. The env editor fetches values from the backend and supports masking secrets before saving them back to `.env`. Saving writes `.env`, `.env.template.json`, `docker-compose.yml`, `codex.runtime.json` and `codexbooster.config.json` for repeatable setups. See [docs/setup-guide.md](docs/setup-guide.md) for the full list of environment variables required for HipCortex, OpenAI, Stripe and deployment targets along with an example `.env.template.json` to help deploy securely.

### Memory Snapshots

All agent reasoning is captured as **versioned memory snapshots** under `hipcortex_logs/`. The API exposes:

- `POST /api/hipcortex/record` – append a snapshot with timestamp and confidence.
- `GET /api/hipcortex/logs?session_id=<id>` – retrieve the full trace.
- `POST /api/hipcortex/rollback` – restore `current_version` to an earlier id.

This allows auditing decisions and exploring diffs across build attempts.

### Artifact Rollback

Run artifacts such as diffs, test results and documentation are saved under
`artifacts/` and mirrored to optional object storage. The helper in
`backend.rollback` can snapshot the directory, tag the current git commit and
restore a previous state:

```python
from backend.rollback import create_snapshot, restore_snapshot

# save artifacts and tag the repo
create_snapshot("release-1")

# later, roll back
restore_snapshot("release-1")
```

By default telemetry is enabled and exports traces/metrics via OTLP to
Tempo/Jaeger and logs to Loki. Environment variables `OTLP_TRACES_ENDPOINT`,
`OTLP_METRICS_ENDPOINT` and `OTLP_LOGS_ENDPOINT` customise the targets.

### Exporting the Frontend

The API exposes a convenient route to download the current frontend as a
zip archive.  Trigger a build from the `/export` page or call:

- `GET /export/frontend` – returns `frontend.zip` ready for deployment.

This can be used in CI/CD workflows or to share a snapshot of the UI with
team members.

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

The [Agentic Framework](docs/agentic-framework.md) summarises best-practice prompting strategies inspired by the Y Combinator "State-Of-The-Art Prompting For AI Agents" episode.

[Use Cases](docs/use_cases.md) page lists example prompts by value stream.

