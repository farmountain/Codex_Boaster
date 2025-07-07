# End-to-End Test Plan

This document describes a typical user journey through Codex Booster. The goal is to verify that each phase works as expected, from installation to deployment. The references to API routes correspond to the FastAPI backend while UI components map to the Next.js dashboard.

## Installation

1. Clone the repository and install Python dependencies:
   ```bash
   git clone https://github.com/your-org/codex-booster.git
   cd codex-booster
      Get-ChildItem -Directory | Where-Object { $_.Name -match 'venv|env' } #(powershell)
   ls -d */ | grep -E 'venv|env' #(Linux terminal)
   .\.venv\Scripts\Activate
   pip install -r requirements.txt
   ```
   **Expected result:** `uvicorn` and `fastapi` are available.
2. Install frontend packages:
   ```bash
   cd frontend && npm install
   ```
   **Expected result:** `node_modules/` is created with React and Jest.
3. Launch the services in separate terminals from the project root:
   ```bash
   uvicorn backend.main:app --reload
   npm run dev --prefix frontend
   ```
   If you run `uvicorn` from another directory, Python may fail to
   locate the `backend` package and raise `ModuleNotFoundError`.
   **Expected result:** API docs at `http://localhost:8000/docs` and the dashboard at `http://localhost:3000`.

## Configuration

1. Open the **Configure Environment** page in the dashboard.
2. Choose runtime versions using the **RuntimeSelector** component.
3. Add environment variables and save the form.
   - **API route:** `POST /api/config/env`
   - **Expected result:** `.env` and `docker-compose.yml` are written and values appear in the UI.

## Project Creation

1. On the dashboard, select **New Project**.
2. Enter a repository name and language runtime.
3. Upload any setup script or secrets if required.
   - **API route:** `POST /api/repo-init`
   - **Expected result:** a new project entry appears in the workspace list with status `initialized`.

## Agent Interactions

### Planning
1. Provide a feature description in the **Planner** text area.
2. Click **Plan** which triggers `POST /architect`.
   - **Expected result:** the **ReasoningPanel** shows a step‑by‑step plan and the API returns a `plan_id`.

### Building
1. Review the generated plan and click **Build**.
2. The browser sends build instructions to `POST /builder`.
   - **Expected result:** files are created under the project folder and the build log appears in the workspace panel.

### Testing
1. Press **Test** after the build finishes.
2. The **TesterAgent** runs via `POST /run-tests`.
   - **Expected result:** test results stream to the **TerminalPanel** and a pass/fail badge is shown.

### Reflexion
1. If tests fail, select **Improve** to invoke `POST /reflexion`.
2. The panel lists confidence scores and suggested fixes.
   - **Expected result:** new reasoning logs are recorded and failures are summarised.

### Deployment
1. When all tests pass, open **DeployPanel** and fill in the host details.
2. Submit the form which calls `POST /api/deploy`.
   - **Expected result:** a deployment preview link and logs appear. `POST /api/deploy/rollback` can revert to an earlier snapshot if needed.

## Documentation Generation

1. Switch to **DocAgent** and click **Generate Docs**.
   - **API route:** `POST /api/docs`
   - **Expected result:** markdown files are created under `docs/generated/` and listed in the UI.

## Marketplace Access

1. Visit the **Marketplace** page.
2. Use `GET /api/marketplace` to list connectors.
3. Enable or disable plugins using `POST /api/marketplace/toggle/{plugin_id}`.
   - **Expected result:** plugin status updates and events are logged to HipCortex.

## Billing

1. Open the **Billing** settings.
2. Choose a subscription plan and submit.
   - **API route:** `POST /charge`
   - **Expected result:** a Stripe checkout session URL is returned and charges are recorded.

## Team Collaboration

1. Invite a teammate from the **Project Settings** panel.
2. Shared sessions appear in the workspace.
   - **Expected result:** both users can see reasoning logs in real time and update the project concurrently.

## Accessibility Checks

1. Run the `AccessibilityChecker` from the command line:
   ```bash
   node scripts/accessibility.js
   ```
2. Verify that all interactive elements have labels and sufficient contrast.
   - **Expected result:** the script reports zero violations.

