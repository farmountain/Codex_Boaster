from typing import Any, Dict

from opentelemetry import trace

tracer = trace.get_tracer(__name__)


def call_tool(name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Minimal MCP tool invocation that emits an OpenTelemetry span.

    In a real system this would dispatch to an MCP runtime. Here we simply
    echo the payload back while recording the call for tracing purposes.
    """

    with tracer.start_as_current_span("tool") as span:
        span.set_attribute("tool.name", name)
        span.set_attribute("tool.payload", str(payload))
        return {"tool": name, "payload": payload}
