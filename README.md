# Codex Booster

This repository contains the scaffolding for **Codex Booster**, an AI-native platform that orchestrates multiple agents to convert user goals into working software. The implementation integrates with **HipCortex** for all memory and reflexion functionality. See `docs/README.md` for an overview of the architecture and development roadmap.

## Frontend

The `frontend` directory contains a minimal Next.js application with pages for the landing site, pricing, dashboard, and contact information. The dashboard integrates with the FastAPI backend and demonstrates Clerk authentication and Stripe billing via the `/charge` endpoint.

## Development

Run all automated tests with the helper script:

```bash
./scripts/test_all.sh
```

This executes Jest for the Node code and Pytest for the backend.
