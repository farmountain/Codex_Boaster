# Architecture

```
codex-booster/
├── backend/
│   ├── main.py            # FastAPI entry point
│   ├── agents/            # Architect, Builder, Tester, Reflexion, Exporter, Monetizer
│   ├── integrations/      # HipCortex bridge
│   ├── services/          # AUREUS helpers and build workflow
│   └── terminal_runner.py # execute setup commands
├── frontend/              # Next.js application
└── docs/                  # Documentation
```

The backend exposes a FastAPI API with one route per agent.  `hipcortex_bridge.py`
provides a single interface to HipCortex for logging and memory snapshots.  The
`build_test_cycle` helper orchestrates BuilderAgent, TesterAgent and
ReflexionAgent to implement the TDD loop.

The Next.js frontend exposes a sidebar with a project switcher, an **Agent
Panel** for conversational commands and a real‑time workspace list.  Each
project stores its runtime configuration (Python, Node, Rust, etc.) and secrets
in HipCortex so that the agents always operate with the latest context.  Test
results, confidence scores and retry history are displayed in the Reflexion
panel alongside a HipCortex memory timeline. The panel fetches `/reflexion/logs`
from the API which returns the agent's chain-of-thought traces and confidence
metrics.

Additional helper modules are planned for configuration and deployment:

- **Config Agent** – generates `.env`, `docker-compose.yml` and other runtime files from user input. The agent parses `.env.template.json`, validates values and writes runtime artifacts. A pre-run validator feeds missing variables to the ReflexionAgent for user feedback.
- **Repo‑Init Agent** – scaffolds GitHub repositories with CI hooks.
- **Deploy Agent** – deploys the generated project to Vercel, Render or other
  hosts.
- **Integration Agent** – detects API/SDK usage and wires credentials.
- **Test‑Suite Agent** – produces SIT/UAT scripts on top of unit tests.
- **TerminalRunnerService** – executes setup commands and streams logs to the UI.

- **Marketplace Service** – exposes external components (MCP servers, LLM adapters, database connectors).


Each agent has a dedicated router so the API can be consumed individually or
via the `/builder/build_and_test` endpoint which drives the full build/test
cycle. The frontend Dashboard component calls these endpoints and displays the
latest reasoning traces stored in HipCortex.

The frontend consumes these API endpoints to display plans, build results and
billing status to the user.

## Agentic Framework Overview

Codex Booster applies an agentic software development framework derived from the Y Combinator "State-Of-The-Art Prompting For AI Agents" podcast. Each value stream step maps to a dedicated agent and prompt technique, as outlined in [agentic-framework.md](agentic-framework.md). The framework emphasises Parahelp SOP prompts for planning, prompt folding during build, debug logging for tests, reflexion chains for improvement and an orchestrator for deployment.
