MARKETPLACE_COMPONENTS = [
    {"name": "Ollama LLM", "type": "llm", "url": "https://ollama.ai"},
    {"name": "vLLM", "type": "llm", "url": "https://vllm.ai"},
    {"name": "MCP Server", "type": "mcp", "url": "https://example.com/mcp"},
    {"name": "A2A Protocol Adapter", "type": "protocol", "url": "https://example.com/a2a"},
    {"name": "Supabase", "type": "database", "url": "https://supabase.io"},
    {"name": "Firebase", "type": "database", "url": "https://firebase.google.com"},
    {"name": "MongoDB Atlas", "type": "database", "url": "https://mongodb.com"},
]


def list_components():
    """Return available marketplace components."""
    return MARKETPLACE_COMPONENTS
