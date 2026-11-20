"""
Implementation of monitoring-related functions and classes for the retrieval system.
JSON Logger, MetricsCollector, and other monitoring utilities are defined here.
MetricsCollector using Prometheus for collecting and exposing metrics for monitoring and alerting.
"""
import logging
import json
import time
from datetime import datetime, timezone
from functools import wraps
from typing import Any, Callable, Dict, Optional

class JSONFormatter(logging.Formatter):
    """
    Custom JSON formatter for logging.
    """

    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line_no": record.lineno,
        }

        if hasattr(record, "extra_data"):
            log_record["extra_data"] = record.extra_data
        return json.dumps(log_record)

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with JSON formatting.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

class RequestTimer:
    """
    Context manager for timing code execution.
    """

    def __init__(self, logger: logging.Logger, operation_name: str):
        self.logger = logger
        self.operation_name = operation_name

    def __enter__(self):
        self.start_time = time.time()

    def __exit__(self, exc_type, exc_value, traceback):
        elapsed_time = time.time() - self.start_time
        self.logger.info(
            f"Operation '{self.operation_name}' completed in {elapsed_time:.4f} seconds."
        )