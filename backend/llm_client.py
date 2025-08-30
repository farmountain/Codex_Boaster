from typing import Dict
import os
import httpx

from .credential_helper import get_api_key


def call_ollama_or_openai(prompt: str) -> str:
    """Call Ollama or OpenAI depending on env vars.

    Falls back to a local stub when no configuration is provided.
    """
    ollama_url = get_api_key("OLLAMA_URL")
    openai_key = get_api_key("OPENAI_API_KEY")

    if ollama_url:
        model = os.getenv("OLLAMA_MODEL", "codex")
        resp = httpx.post(
            f"{ollama_url}/api/generate",
            json={"model": model, "prompt": prompt},
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        return data.get("response") or data.get("choices", [{}])[0].get("text", "")

    if openai_key:
        model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        resp = httpx.post(
            "https://api.openai.com/v1/chat/completions",
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
            },
            headers={"Authorization": f"Bearer {openai_key}"},
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]

    # cost-saving stub when no API key provided
    return "# generated code\n"


def generate_code_snippet(language: str, purpose: str, context: str) -> str:
    prompt = f"You are an expert {language} developer.\n\nTask: {purpose}\nContext:\n{context}\n\nGenerate production-ready code for this."
    return call_ollama_or_openai(prompt)


def generate_test_cases(code: str, test_type: str = "unit") -> str:
    """Generate test cases for given code."""
    prompt = f"Write {test_type} tests for the following code:\n\n{code}\n"
    return call_ollama_or_openai(prompt)


def generate_improvement_suggestions(test_log: str, code: str, context: dict):
    """Return structured improvement suggestions using a CoT prompt."""
    prompt = f"""
You are a CoT-based reasoning agent using the AUREUS framework.

Analyze this test log and suggest 3–5 concrete improvement steps with reasoning:

🧪 Test Log:
{test_log}

💻 Code:
{code}

💡 Output:
- Chain-of-thought reasoning per step
- Fixes or refactoring ideas
- Confidence level (1–10)

Respond in JSON:
{{
  "steps": [
    {{ "step": "...", "why": "...", "fix": "...", "confidence": 8 }},
    ...
  ]
}}
"""
    return call_ollama_or_openai(prompt)


def generate_docs(files: Dict[str, str], context: Dict):
    prompt = f"""
You are a technical writer agent.

Given the following code files and context from memory (tests, plan, config), generate:
- 📘 README.md with setup, features, and modules
- 🧠 architecture.md with system design
- ⚙️ api.md with endpoint details
- 🧪 tests.md with coverage explanation

Files:
{list(files.keys())}

Code + Context:
{str(context)[:4000]}

Respond as JSON:
{{
  "README.md": "...",
  "architecture.md": "...",
  "api.md": "...",
  "tests.md": "..."
}}
"""
    return call_ollama_or_openai(prompt)
