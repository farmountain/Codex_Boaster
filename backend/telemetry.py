import os
from typing import Optional
from opentelemetry import trace, metrics, _logs
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.http.metric_exporter import (
    OTLPMetricExporter,
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter as HTTPSpanExporter,
)
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter


def _endpoint(env: str, default: str) -> str:
    return os.getenv(env, default)


def setup_telemetry(service_name: Optional[str] = None) -> None:
    """Configure OTLP exporters for traces, metrics and logs.

    Traces and metrics are exported to Tempo/Jaeger, logs are sent to Loki.
    Endpoints can be customised via environment variables:
    ``OTLP_TRACES_ENDPOINT``, ``OTLP_METRICS_ENDPOINT`` and
    ``OTLP_LOGS_ENDPOINT``. ``OTEL_SERVICE_NAME`` overrides the default
    service name.
    """

    resource = Resource.create(
        {SERVICE_NAME: service_name or os.getenv("OTEL_SERVICE_NAME", "codex-boaster")}
    )

    # --- Tracing ---
    trace_provider = TracerProvider(resource=resource)
    span_exporter = HTTPSpanExporter(
        endpoint=_endpoint("OTLP_TRACES_ENDPOINT", "http://tempo:4318/v1/traces"),
    )
    trace_provider.add_span_processor(BatchSpanProcessor(span_exporter))
    trace.set_tracer_provider(trace_provider)

    # --- Metrics ---
    metric_exporter = OTLPMetricExporter(
        endpoint=_endpoint("OTLP_METRICS_ENDPOINT", "http://tempo:4318/v1/metrics"),
    )
    reader = PeriodicExportingMetricReader(metric_exporter)
    meter_provider = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(meter_provider)

    # --- Logging ---
    logger_provider = LoggerProvider(resource=resource)
    log_exporter = OTLPLogExporter(
        endpoint=_endpoint("OTLP_LOGS_ENDPOINT", "http://loki:4318/v1/logs"),
    )
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
    _logs.set_logger_provider(logger_provider)


__all__ = ["setup_telemetry"]
