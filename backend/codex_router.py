"""Prompt router for ChatAgent requests."""

from backend.llm_client import call_ollama_or_openai


def fallback_llm_response(prompt: str) -> str:
    """Fallback LLM call when no specialised agent matches."""
    return call_ollama_or_openai(prompt)


def route_prompt_to_agent(prompt: str, history=None):
    """Route prompt to an appropriate agent based on simple keyword rules."""
    history = history or []
    lower = prompt.lower()
    if "plan" in lower:
        return {"plan": f"Plan for {prompt}"}, {"agent": "ArchitectAgent"}
    elif "test" in lower:
        return "# tests", {"agent": "TestSuiteAgent"}
    elif "fix" in lower or "error" in lower:
        return "refactor suggestions", {"agent": "ReflexionAgent"}
    else:
        return fallback_llm_response(prompt), {"agent": "ChatAgent"}
