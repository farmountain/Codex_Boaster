# Use Cases by Value Stream

Codex Booster automates the full software development lifecycle. The table below summarises common value stream activities and example prompts that trigger the responsible agents.

| Value Stream Activity | Features & Agents | Example Prompt |
|----------------------|------------------|----------------|
| **Plan** | `ArchitectAgent` analyses the goal and produces module plans recorded in HipCortex. | "Plan an AI planner with Stripe billing" |
| **Configure** | `Config-Agent` creates `.env`, `docker-compose.yml` and Supabase/Clerk/Stripe keys. | "Setup project env with Postgres and Clerk" |
| **Repo Init** | `Repo-Init Agent` scaffolds a GitHub repo with CI hooks and templates. | "Create repo for SaaS billing dashboard" |
| **Build** | `BuilderAgent` generates code from tests. | "Write code to satisfy these Jest tests" |
| **Test** | `TesterAgent` runs unit and integration suites; `Test-Suite Agent` generates SIT/UAT flows. | "Run integration tests for Stripe checkout" |
| **Reflexion** | `ReflexionAgent` applies AUREUS loop to failed output to refine instructions. | automatic |
| **Deploy** | `Deploy-Agent` provisions preview environments via GitHub Actions and Vercel/Render. | "Deploy latest build" |
| **Document** | `Doc-Agent` writes usage instructions and inline docs. | "Generate README for the repo" |
| **Chat / Improve** | `Chat-Agent` presents reasoning traces and accepts user feedback. | Interact in dashboard chat |
| **Monetize** | `MonetizerAgent` records usage and charges through Stripe. | automatic |
| **Marketplace** | `Marketplace Service` lists external connectors and tools. | "Show available LLM adapters" |

These activities combine to deliver an autonomous build-test-deploy cycle with persistent memory via HipCortex.
