import sys
import logging
import structlog
from pythonjsonlogger import jsonlogger
from datetime import datetime
from typing import Any, Dict

# Configure standard logging
json_handler = logging.StreamHandler(sys.stdout)
json_handler.setFormatter(jsonlogger.JsonFormatter())

logging.basicConfig(
    level=logging.INFO,
    handlers=[json_handler]
)

# Configure structlog pre-processors
pre_chain = [
    structlog.contextvars.merge_contextvars,
    structlog.processors.add_log_level,
    structlog.processors.TimeStamper(fmt="iso", utc=True),
    structlog.processors.StackInfoRenderer(),
    structlog.processors.format_exc_info,
]

# Configure structlog
structlog.configure(
    processors=pre_chain + [
        structlog.processors.JSONRenderer(serializer=lambda obj: obj)
    ],
    logger_factory=structlog.PrintLoggerFactory(),
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    cache_logger_on_first_use=True,
)

def get_logger(name: str) -> structlog.BoundLogger:
    """Get a structured logger instance."""
    return structlog.get_logger(name)

def log_request_info(logger: structlog.BoundLogger, request_id: str, **kwargs: Any) -> None:
    """Log request information with structured data."""
    log_data = {
        "request_id": request_id,
        "timestamp": datetime.utcnow().isoformat(),
        **kwargs
    }
    logger.info("request_processed", **log_data)

def log_error(logger: structlog.BoundLogger, error: Exception, context: Dict[str, Any]) -> None:
    """Log error information with structured data."""
    log_data = {
        "error_type": type(error).__name__,
        "error_message": str(error),
        "timestamp": datetime.utcnow().isoformat(),
        **context
    }
    logger.error("error_occurred", **log_data)

def log_api_call(
    logger: structlog.BoundLogger,
    service: str,
    operation: str,
    duration_ms: float,
    success: bool,
    **kwargs: Any
) -> None:
    """Log external API call information."""
    log_data = {
        "service": service,
        "operation": operation,
        "duration_ms": duration_ms,
        "success": success,
        "timestamp": datetime.utcnow().isoformat(),
        **kwargs
    }
    logger.info("api_call", **log_data) 