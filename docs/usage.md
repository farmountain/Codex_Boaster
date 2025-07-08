# Usage Guide

This short guide explains how to try Codex Booster locally. The platform exposes
an API powered by FastAPI and a small Next.js interface. The dashboard
presents **Plan**, **Build**, **Test** and **Deploy** actions that drive the
agent workflow. When creating a project you can choose the language runtime
(Python, Node.js, Rust, Bun, Java, Swift or Ruby) and provide any secrets
inline. A drop‑down also lets you upload a setup script or open an interactive
terminal.

The recommended workflow follows the [Agentic Framework](agentic-framework.md):
start with ParahelpPlannerAgent to capture requirements, let PromptBoosterAgent
generate code using prompt folding, review gaps through DebugLogAgent, then
iterate via ChainReflexionAgent. Prompts that pass tests are stored by
PromptLibraryAgent and orchestrated into deployments by FDEOrchestratorAgent.

Example prompts:

- *"Build an AI planner with Stripe billing"* – triggers the Planner and Repo‑Init agents.
- *"Deploy latest build"* – calls the Deploy agent to provision a preview environment.
- *"Show marketplace components"* – lists available MCP servers and LLM adapters.


## Backend

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the API server from the repository root:
   ```bash
   uvicorn backend.main:app --reload
   ```
   Running this command outside the root directory may cause a
   `ModuleNotFoundError` for the `backend` package.
3. Open `http://localhost:8000/docs` to inspect the available endpoints.

### LLM Configuration

Set `OLLAMA_URL` (and optional `OLLAMA_MODEL`) to run a local model.
If `OPENAI_API_KEY` is configured, the client uses OpenAI's API with the
`OPENAI_MODEL` environment variable (default `gpt-3.5-turbo`). When neither is
set the system falls back to a small offline stub so tests run without network
access.

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
   - Check the **Reflexion** panel for agent confidence and retry history.
   - The **Workspace** list shows runtime tags and build status for each repo.

## Running Tests

Execute all Python and frontend tests from the project root:

```bash
pytest
npm test --silent
cd frontend && npm test --silent && cd ..
```

The dashboard fetches results from `/test_results` and displays the last
improvement suggestion from `/improvement_suggestion`.

### UI Testing

Run `npm test --silent` in both the repository root and `frontend/` directory to
execute the Jest suites.  These include simple UAT flows for the Plan selector
and reasoning panel components.  All tests should pass before deploying a new
project.

### Exporting the Frontend

Download a zipped snapshot of the UI using:

```bash
curl -O http://localhost:8000/export/frontend
```

The Export page exposes the same functionality via the browser.
