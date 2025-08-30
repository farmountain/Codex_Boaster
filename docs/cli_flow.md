# CLI Flow: `codex init` and `codex run`

This example demonstrates how to initialise a project and execute a sample plan using the `codex-cli` tool. The plan streams execution to a Goose runtime and can invoke MCP tools defined in `shared/tool_schemas.json`.

## Initialise a project

```bash
codex init demo-project
```

This registers the project with the Codex Boaster backend and creates initial configuration files.

## Execute a plan

1. Save the sample plan:

   ```bash
   cp examples/sample_plan.json plan.json
   ```

2. Run the plan and stream output through Goose:

   ```bash
   codex run demo-project --ws-url ws://localhost:9001/run < plan.json
   ```

The CLI posts the plan to the backend, which coordinates Goose and available MCP tools to perform each task. Output from Goose is printed to the console.
