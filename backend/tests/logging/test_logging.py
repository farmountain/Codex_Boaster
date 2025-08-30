import pytest
import logging
import logging.handlers
import os
from datetime import datetime
import json
from backend.logging.config import (
    get_log_level,
    setup_logger,
    setup_audit_logger,
    setup_performance_logger
)
from backend.logging.structured import StructuredLogger, AuditLogger, PerformanceLogger
from backend.logging.monitoring import (
    monitor_performance,
    monitor_api_endpoint,
    monitor_database_query,
)

def test_log_level():
    # Test default log level
    assert get_log_level() == logging.INFO
    
    # Test custom log level
    os.environ["LOG_LEVEL"] = "DEBUG"
    assert get_log_level() == logging.DEBUG
    
    # Test invalid log level
    os.environ["LOG_LEVEL"] = "INVALID"
    assert get_log_level() == logging.INFO

def test_logger_setup(monkeypatch):
    # Mock RotatingFileHandler and StreamHandler to avoid file I/O during tests
    monkeypatch.setattr(logging.handlers, "RotatingFileHandler", lambda *args, **kwargs: logging.StreamHandler())
    monkeypatch.setattr(logging, "StreamHandler", lambda *args, **kwargs: logging.StreamHandler())
    logger = setup_logger("test")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test"
    assert logger.level == logging.INFO
    
    # Check handlers
    assert len(logger.handlers) == 2
    handlers = [type(h) for h in logger.handlers]
def test_audit_logger_setup(monkeypatch):
    monkeypatch.setattr(logging.handlers, "RotatingFileHandler", lambda *args, **kwargs: logging.StreamHandler())
    audit_logger = setup_audit_logger()
    assert isinstance(audit_logger, logging.Logger)
    assert audit_logger.name == "audit"
    assert audit_logger.level == logging.INFO
    
    # Check handlers
    assert len(audit_logger.handlers) == 1
    assert isinstance(audit_logger.handlers[0], logging.StreamHandler)
def test_performance_logger_setup(monkeypatch):
    monkeypatch.setattr(logging.handlers, "RotatingFileHandler", lambda *args, **kwargs: logging.StreamHandler())
    perf_logger = setup_performance_logger()
    assert isinstance(perf_logger, logging.Logger)
    assert perf_logger.name == "performance"
    assert perf_logger.level == logging.INFO
    
    # Check handlers
    assert len(perf_logger.handlers) == 1
    assert isinstance(perf_logger.handlers[0], logging.StreamHandler)

def test_structured_logging():
    logger = StructuredLogger("test")
    
    # Test info log
    test_message = "Test info message"
    logger.info(test_message, key="value")
    
    # Test error log
    test_error = "Test error message"
    logger.error(test_error, error_type="test")

def test_audit_logging():
    audit_logger = AuditLogger()
    
    # Test audit log
    audit_logger.log(
        user="test_user",
        action="test_action",
        resource="test_resource",
        status="success",
        message="Test audit message"
    )

def test_performance_logging():
    perf_logger = PerformanceLogger()
    
    # Test performance log
    perf_logger.log(
        component="test",
        metric="test_metric",
        value=100,
        message="Test performance message"
    )

def test_monitor_performance():
    @monitor_performance("test", "test_metric")
    def test_function():
        return "success"
    
    result = test_function()
    assert result == "success"

def test_monitor_api_endpoint():
    @monitor_api_endpoint("test_endpoint")
    def test_endpoint():
        return {"status": "success"}
    
    result = test_endpoint()
    assert result["status"] == "success"

def test_monitor_database_query():
    @monitor_database_query("test_query")
    def test_query():
        return [1, 2, 3]
    
    result = test_query()
    assert len(result) == 3
