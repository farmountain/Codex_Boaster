# Architecture

```
codex-booster/
├── backend/
│   ├── main.py            # FastAPI entry point
│   ├── agents/            # Architect, Builder, Tester, Reflexion, Exporter, Monetizer
│   ├── integrations/      # HipCortex bridge
│   └── services/          # AUREUS helpers and build workflow
├── frontend/              # Next.js application
└── docs/                  # Documentation
```

The backend exposes a FastAPI API with one route per agent.  `hipcortex_bridge.py`
provides a single interface to HipCortex for logging and memory snapshots.  The
`build_test_cycle` helper orchestrates BuilderAgent, TesterAgent and
ReflexionAgent to implement the TDD loop.

Each agent has a dedicated router so the API can be consumed individually or
via the `/builder/build_and_test` endpoint which drives the full build/test
cycle. The frontend Dashboard component calls these endpoints and displays the
latest reasoning traces stored in HipCortex.

The frontend consumes these API endpoints to display plans, build results and
billing status to the user.
