import json
from typing import Dict, Any
from datetime import datetime
from backend.logging.config import get_logger

class StructuredLogger:
    def __init__(self, name: str = __name__):
        self.logger = get_logger(name)

    def log(self, level: str, message: str, **kwargs: Any) -> None:
        """Log a structured message."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level.upper(),
            "message": message,
            "context": kwargs
        }
        self.logger.log(
            getattr(logging, level.upper()),
            json.dumps(log_entry, default=str)
        )

    def info(self, message: str, **kwargs: Any) -> None:
        self.log("info", message, **kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        self.log("error", message, **kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        self.log("warning", message, **kwargs)

    def debug(self, message: str, **kwargs: Any) -> None:
        self.log("debug", message, **kwargs)

    def critical(self, message: str, **kwargs: Any) -> None:
        self.log("critical", message, **kwargs)

class AuditLogger:
    def __init__(self):
        self.logger = get_logger("audit")

    def log(self, user: str, action: str, resource: str, status: str, message: str) -> None:
        """Log an audit event."""
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "user": user,
            "action": action,
            "resource": resource,
            "status": status,
            "message": message
        }
        self.logger.info(json.dumps(audit_entry, default=str))

class PerformanceLogger:
    def __init__(self):
        self.logger = get_logger("performance")

    def log(self, component: str, metric: str, value: Any, message: str) -> None:
        """Log performance metrics."""
        perf_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "component": component,
            "metric": metric,
            "value": value,
            "message": message
        }
        self.logger.info(json.dumps(perf_entry, default=str))
