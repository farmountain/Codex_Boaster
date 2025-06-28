def call_ollama_or_openai(prompt: str) -> str:
    """Placeholder LLM call for tests."""
    # In a real implementation this would call Ollama or OpenAI APIs.
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
