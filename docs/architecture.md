# Architecture

```
codex-booster/
├── backend/
│   ├── main.py
│   ├── agents/
│   ├── integrations/
│   └── ...
├── frontend/
│   └── ...
└── docs/
```

The backend exposes a FastAPI application with modular agents. Each agent uses `hipcortex_bridge.py` for memory and reflexion.
