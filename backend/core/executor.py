"""
Tool execution orchestration.

Single entry point for all tool executions. Handles:
- Request ID generation
- Context creation
- Logging
- Error handling
- Result wrapping
"""
import uuid
import traceback
from datetime import datetime
from typing import Dict, Any
from backend.core.registry import get_registry
from backend.core.base_tool import ExecutionContext
from backend.lib.result import Result
from backend.lib.logger import get_logger
from backend.lib.errors import (
    ToolExecutionError,
    ToolNotFoundError
)


class ToolExecutor:
    """
    Centralized tool execution with observability.

    The executor is the single entry point for all tool executions.
    It provides:
    - Unique request IDs for tracing
    - Structured logging with context
    - Consistent error handling
    - Result wrapping
    """

    def __init__(self):
        """Initialize executor with registry."""
        self.registry = get_registry()

    def execute(
        self,
        user,
        tool_path,
        params
    ):
        """
        Execute a tool with full observability.

        Args:
            user: User executing the tool
            tool_path: Full tool path (e.g., "RAD/ingestor/timeline")
            params: Tool parameters

        Returns:
            Result object (success or error)
        """
        # Generate unique request ID
        request_id = str(uuid.uuid4())

        # Create context
        timestamp = datetime.utcnow()
        logger = get_logger(
            tool_path=tool_path,
            user=user,
            request_id=request_id
        )

        context = ExecutionContext(
            request_id=request_id,
            user=user,
            timestamp=timestamp,
            tool_path=tool_path,
            params=params,
            logger=logger
        )

        # Log execution start
        logger.info(
            f"Tool execution started: {tool_path}",
            extra={'params': params}
        )

        try:
            # Get tool from registry
            tool = self.registry.get_tool(tool_path)

            # Execute tool
            start_time = datetime.utcnow()
            data = tool.run(context, **params)
            duration = (datetime.utcnow() - start_time).total_seconds()

            # Log success
            logger.info(
                f"Tool execution completed in {duration:.2f}s",
                extra={'duration': duration}
            )

            return Result.success_result(data=data, request_id=request_id)

        except ToolNotFoundError as e:
            # Tool doesn't exist
            logger.error(f"Tool not found: {e}")
            return Result.error_result(
                message=str(e),
                request_id=request_id,
                error_type="ToolNotFound",
                user_message=f"Tool '{tool_path}' does not exist"
            )

        except ToolExecutionError as e:
            # Expected business error
            logger.warning(f"Tool execution failed: {e}")
            return Result.error_result(
                message=str(e),
                request_id=request_id,
                error_type=e.__class__.__name__,
                user_message=e.user_message
            )

        except Exception as e:
            # Unexpected error
            tb = traceback.format_exc()
            logger.error(
                f"Unexpected error during tool execution: {e}",
                exc_info=True
            )
            return Result.error_result(
                message=str(e),
                request_id=request_id,
                error_type="UnexpectedError",
                user_message="An unexpected error occurred. Please contact support.",
                traceback=tb
            )


# Global singleton
_executor = None


def get_executor():
    """
    Get the global ToolExecutor instance.

    Returns:
        Singleton ToolExecutor instance
    """
    global _executor
    if _executor is None:
        _executor = ToolExecutor()
    return _executor
