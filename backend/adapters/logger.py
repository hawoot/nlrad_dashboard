"""
Logger adapter - SWAP THIS AT WORK

Currently uses local JSON/text logger implementation.
To use work environment: Comment out LOCAL section, uncomment WORK section below.
"""
from pathlib import Path

# ==============================================================================
# LOCAL IMPLEMENTATION (for development)
# ==============================================================================

import logging
import json
import sys
from datetime import datetime
from typing import Dict, Any

# Local configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "json"  # json or text
LOG_FILE = Path(__file__).parent.parent.parent / "logs" / "dashboard.log"


class ContextFilter(logging.Filter):
    """
    Logging filter that adds execution context to log records.
    """
    def __init__(self, context):
        super().__init__()
        self.context = context

    def filter(self, record):
        """Add context fields to the log record."""
        for key, value in self.context.items():
            setattr(record, key, value)
        return True


class JSONFormatter(logging.Formatter):
    """
    Format log records as JSON for structured logging.
    """
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
        }

        # Add context fields if present
        for attr in ['user', 'request_id', 'tool_path']:
            if hasattr(record, attr):
                log_data[attr] = getattr(record, attr)

        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)

        return json.dumps(log_data)


class TextFormatter(logging.Formatter):
    """
    Format log records as human-readable text.
    """
    def format(self, record):
        context = []
        for attr in ['user', 'request_id', 'tool_path']:
            if hasattr(record, attr):
                context.append(f"{attr}={getattr(record, attr)}")

        context_str = f" [{' '.join(context)}]" if context else ""

        return f"{record.levelname}: {record.getMessage()}{context_str}"


def configure_root_logger():
    """
    Configure the root logger for the application.

    Called once during application startup.
    """
    # Create logs directory if it doesn't exist
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, LOG_LEVEL.upper()))

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    # File handler
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(logging.DEBUG)

    # Select formatter based on LOG_FORMAT
    if LOG_FORMAT.lower() == 'json':
        formatter = JSONFormatter()
    else:
        formatter = TextFormatter()

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)


def get_logger(
    tool_path=None,
    user=None,
    request_id=None
):
    """
    Get a logger with pre-configured context.

    All log statements from this logger will automatically include
    the provided context fields.

    Args:
        tool_path: Path of the tool being executed
        user: User executing the tool
        request_id: Unique identifier for this execution

    Returns:
        Logger with context filter applied
    """
    logger = logging.getLogger(__name__)

    # Build context dictionary
    context = {}
    if tool_path:
        context['tool_path'] = tool_path
    if user:
        context['user'] = user
    if request_id:
        context['request_id'] = request_id

    # Add context filter if we have context
    if context:
        context_filter = ContextFilter(context)
        logger.addFilter(context_filter)

    return logger


# ==============================================================================
# WORK IMPLEMENTATION (commented out - uncomment when deploying to work)
# ==============================================================================

# from your_work_package.logging import (
#     configure_logger as configure_root_logger,
#     get_logger,
# )
#
# LOG_LEVEL = "INFO"  # Or from work config
# LOG_FORMAT = "json"  # Or from work config
