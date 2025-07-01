# Technical Solution

The system follows a TDD-first workflow guided by six cooperating agents:

1. **ArchitectAgent** breaks a user goal into modules and logs the plan to
   HipCortex.
2. **BuilderAgent** generates minimal code to satisfy the tests.
3. **TesterAgent** runs pytest on the generated code.
4. **ReflexionAgent** applies the AUREUS reasoning loop to failed test output and
   updates the BuilderAgent instructions.
5. **ExporterAgent** packages artefacts once tests pass.
6. **MonetizerAgent** records usage and creates Stripe charges.
7. **Config Agent** builds runtime files such as `.env` and `docker-compose.yml`.
8. **Repo‑Init Agent** creates a GitHub repository with CI/CD hooks.
9. **Integration Agent** wires external APIs (Supabase, Clerk, Stripe, etc.).
10. **Test‑Suite Agent** generates SIT and UAT plans.
11. **Deploy Agent** provisions preview deployments.
12. **Doc Agent** writes usage documentation and UX walkthroughs.
13. **Chat Agent** exposes reasoning traces and accepts instructions from the UI.
14. **Marketplace Service** manages third-party connectors such as MCP servers, A2A adapters and LLM APIs.

Agent interactions rely on chain-of-thought prompts recorded in HipCortex. The
AUREUS framework evaluates failed attempts and feeds new instructions back to
the Builder. Multiple language runtimes are preinstalled (Python, Node.js,
Rust, Bun, Java, Swift and Ruby) so users can mix stacks per project.


All memory and reasoning context flows through `hipcortex_bridge.py`.  The
`build_test_cycle` function encapsulates the round‑trip from code generation to
testing and reflexion.

Each step is logged to HipCortex so that the AUREUS reflexion loop can analyse
failures and propose new builder instructions. This chain‑of‑thought history is
available in the dashboard via the *ReasoningPanel* component.

The dashboard shows a list of workspaces with status badges and provides a chat
interface that triggers individual agents. A terminal panel allows rerunning
tests or executing setup scripts directly from the browser. Deployment previews
are launched automatically from CI once the test matrix passes.

The frontend polls `/test_results` and `/improvement_suggestion` to provide live
feedback during the build process.
