# Marketplace Guide

Codex Booster exposes a marketplace where external contributors can publish
integrations such as MCP servers, A2A protocol adapters or LLM connectors.
Each component is reviewed for security and performance before being listed.

## Submitting a Component

1. Fork the repository and add your service under `marketplace/`.
2. Include a manifest describing the endpoints, required credentials and cost.
3. Submit a pull request. A test plan and security checklist must accompany it.

## Best Practices

- **Security**: validate all credentials using environment variables and
  avoid storing secrets in code. Provide a threat model and use OAuth scopes
  where possible.
- **Resilience**: services should retry transient failures and expose health
  endpoints for monitoring.
- **Performance**: implement caching and pagination for heavy APIs. Document
  rate limits clearly.
- **Scalability**: design stateless adapters so Codex Booster can replicate
  your service across workers.
- **Cost Optimisation**: support free tiers or usage-based pricing. Publish
  metrics so users can plan their spend.

By following these guidelines, external vendors can expand Codex Booster with
connectors for Supabase, Firebase, MongoDB and LLM APIs like Ollama or vLLM.
