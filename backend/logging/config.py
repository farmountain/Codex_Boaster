import os
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
from typing import Dict, Any

# Log directory
LOG_DIR = os.getenv("LOG_DIR", "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Log levels
LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}

def get_log_level() -> int:
    """Get log level from environment variable."""
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    return LOG_LEVELS.get(level, logging.INFO)

def setup_logger(name: str) -> logging.Logger:
    """Setup logger with rotating file handler and console handler."""
    logger = logging.getLogger(name)
    logger.setLevel(get_log_level())

    # Create handlers
    file_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, f"{name}.log"),
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    stream_handler = logging.StreamHandler()

    # Create formatters and add to handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger

def get_logger(name: str = __name__) -> logging.Logger:
    """Get or create logger."""
    return logging.getLogger(name)

def setup_audit_logger() -> logging.Logger:
    """Setup audit logger with specific configuration."""
    audit_logger = logging.getLogger("audit")
    audit_logger.setLevel(logging.INFO)

    # Create audit log handler
    audit_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, "audit.log"),
        maxBytes=50*1024*1024,  # 50MB
        backupCount=10
    )

    # Create formatter
    audit_formatter = logging.Formatter(
        '%(asctime)s - %(user)s - %(action)s - %(resource)s - %(status)s - %(message)s'
    )
    audit_handler.setFormatter(audit_formatter)

    audit_logger.addHandler(audit_handler)
    return audit_logger

def setup_performance_logger() -> logging.Logger:
    """Setup performance logger."""
    perf_logger = logging.getLogger("performance")
    perf_logger.setLevel(logging.INFO)

    # Create performance log handler
    perf_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, "performance.log"),
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )

    # Create formatter
    perf_formatter = logging.Formatter(
        '%(asctime)s - %(component)s - %(metric)s - %(value)s - %(message)s'
    )
    perf_handler.setFormatter(perf_formatter)

    perf_logger.addHandler(perf_handler)
    return perf_logger
