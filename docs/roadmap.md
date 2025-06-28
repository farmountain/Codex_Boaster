# Roadmap

1. **Alpha** – Backend agents with HipCortex hooks and test-driven workflow.
2. **Beta** – Next.js frontend, Clerk authentication and basic Stripe billing.
3. **Pro** – Rich reflexion panel, multiple language runtimes and CI deployment.
4. **Enterprise** – Team-based memory isolation, plugin ecosystem and advanced quota management.
5. **Marketplace** – External vendors submit MCP servers, LLM adapters and database connectors. Security and performance guidelines ensure safe deployment.
6. **Full UI/UX** – Sidebar project switcher, agent chat panel, terminal access and workspace list with runtime badges.

## Future Extensions

- Auto-detect language from project structure
- Inline validation of secrets (OPENAI_KEY format)
- Save and reuse previous snapshots from HipCortex memory
- Link config with project IDs in Supabase
- Add feedback loop from Reflexion to BuilderAgent (auto-patch logic)
- Connect this to ChatAgent for “Why did my test fail?” interactions
- Build snapshot explorer for test results + reflexion comparisons
- Extend to include GitHub Actions deploy via CI token
- Automatically infer deploy targets from config_agent + runtime metadata
- Store and replay deploy snapshots in the memory explorer UI
- Trigger DocAgent automatically after a successful build-test loop
- Enable DocAgent to summarize GitHub README + architecture for external repos
- Connect to ChatAgent → "Generate summary of this repo’s architecture"
- Enable voice chat via Whisper API for audio input
- Store all chats as snapshots and link to DocAgent for auto-generated CONVERSATIONS.md
- Let ChatAgent orchestrate a Reflexion → Test → Rebuild loop as a command proxy
