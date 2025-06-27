# Usage Guide

This short guide explains how to try Codex Booster locally. The platform exposes
an API powered by FastAPI and a small Next.js interface. The dashboard
presents **Plan**, **Build**, **Test** and **Deploy** actions that drive the
agent workflow.

Example prompts:

- *"Build an AI planner with Stripe billing"* – triggers the Planner and Repo‑Init agents.
- *"Deploy latest build"* – calls the Deploy agent to provision a preview environment.
- *"Show marketplace components"* – lists available MCP servers and LLM adapters.

## Backend

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the API server:
   ```bash
   uvicorn backend.main:app --reload
   ```
3. Open `http://localhost:8000/docs` to inspect the available endpoints.

## Frontend

1. Navigate to the `frontend` folder and install packages:
   ```bash
   cd frontend && npm install
   ```
2. Launch the development server:
   ```bash
   npm run dev
   ```
3. Visit `http://localhost:3000` and open the **Dashboard**.
   - Write tests in the text area.
   - Use the **Plan**, **Build** and **Test** buttons to drive the
     build/test/reflexion loop.

## Running Tests

Execute all Python and frontend tests from the project root:

```bash
pytest
npm test --silent
cd frontend && npm test --silent && cd ..
```

The dashboard fetches results from `/test_results` and displays the last
improvement suggestion from `/improvement_suggestion`.
