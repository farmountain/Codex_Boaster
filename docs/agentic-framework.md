# Codex Booster Agentic Software Development Framework

This framework distills best practices from the Y Combinator talk **"State-Of-The-Art Prompting For AI Agents"** and adapts them for Codex Booster. It summarises recommended prompting techniques and how multiple agents coordinate tasks.

### \U0001F4DA Key Techniques & Insights

| Technique | Description |
| --- | --- |
| **Parahelp SOP (6-page format)** | Use structured documentation with roles, KPIs and XML-style clarity. |
| **Prompt Folding** | Break down tasks by model type, reducing complexity and cost. |
| **Prompt Library at Scale** | Build a 3,000+ prompt database; think of prompts as a **product knowledge chain**. |
| **Debug Log Agent** | "Taiwan-style debugging": logging what’s missing, unknowns and assumptions. |
| **FDE Agent** | Multi-agent workflow (隔系 Demo): show how different agents coordinate tasks. |

## \U0001F9ED Codex Booster: Agentic Software Development Framework

Using the above best practices, Codex Booster assigns a dedicated agent to each value stream activity. Prompt strategies ensure efficient LLM usage and consistent outputs.

### \U0001F501 Value Stream Activities → Mapped to Agents & Prompt Strategies

| Stage | Activity | Codex Agent | Prompt Strategy/Technique | Description |
| --- | --- | --- | --- | --- |
| \U0001F9E0 **Plan** | Requirements Discovery | `ParahelpPlannerAgent` | **Parahelp SOP** | Use structured prompts with roles, KPIs and XML-format to define dev/test goals. |
| \U0001F3D7️ **Build** | Code Generation | `PromptBoosterAgent` | **Prompt Folding** | Decompose task by LLM type: small → cheap task execution, large → strategic prompts. |
| \U0001F9EA **Test** | Unit & Integration Testing | `DebugLogAgent` | **Debug Log** | Log unknowns and gaps like "Taiwan-style debugging": make the invisible visible. |
| \U0001F501 **Refactor** | Continuous Improvement | `ChainReflexionAgent` | **Prompt Chain** + Metaprompting | Chain feedback from failed tests to improve future prompts. |
| \U0001F680 **Deploy** | Production LLM Prompt Release | `PromptLibraryAgent` | **Prompt Database** | Build a scalable, versioned prompt library (>3,000 prompts). |
| \U0001F9D1‍\U0001F91D **Collaborate** | Agent Orchestration | `FDEOrchestratorAgent` | **隔系 Agent Workflow** | Use multiple specialised agents with clear task separation. |

### \U0001F4E9 Modular Architecture Recommendations

| Layer | Component | Description |
| --- | --- | --- |
| \U0001F4E9 Prompt Layer | Parahelp, Folding, Chain-of-Thought | Modularised prompts by use case, agent and test stage |
| \U0001F9E0 Agent Layer | Planning, Builder, Tester, Reflexion, Orchestrator | Fully agentised based on Codex Booster’s ReAct + Reflexion flow |
| \U0001F4DA Memory Layer | Prompt Library, Debug Logs, SOP Snapshots | Integrate with HipCortex symbolic + episodic memory |
| \u2699️ Runtime Layer | LLM Selector, Prompt Router, Fallback | Deploy small vs large model adaptively with Prompt Folding logic |
| \U0001F4C8 Monitoring Layer | KPI Tracker, Debug Logger | Real-time cost/quality/performance agent logging |

### \U0001F4CC Best Practices

1. **Design with SOP prompts** (Parahelp) – better alignment of dev/test/CI/CD agent outputs.
2. **Optimise cost using Prompt Folding** – choose when to use cheap vs powerful models.
3. **Build reusable prompt assets** – prompt = product; maintain full versioning.
4. **Track test failures as signals** – create logs of gaps in prompt logic and coverage.
5. **Use multi-agent orchestration** – break complex tasks into manageable flows with coordination between agents.

### \U0001F9F1 Example Agent Flow

```
User → ParahelpPlannerAgent → PromptBoosterAgent → BuildOutput
      → DebugLogAgent → ChainReflexionAgent → ImprovedPrompt
      → PromptLibraryAgent → VersionedPromptExport
      → FDEOrchestratorAgent → Coordinated Deployment
```
