"""
Result wrapper for tool executions.

Provides a consistent structure for both successful and failed executions,
eliminating the need for exception handling in the UI layer.
"""
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Result:
    """
    Wrapper for tool execution results.

    Attributes:
        success: True if execution succeeded, False otherwise
        data: Returned data (only set on success)
        error_message: Technical error message for logging
        error_type: Type of error that occurred
        user_message: User-friendly error message for UI
        request_id: Unique identifier for this execution
        traceback: Full stack trace (only for unexpected errors)
    """
    success: bool
    data: Optional[Any] = None
    error_message: Optional[str] = None
    error_type: Optional[str] = None
    user_message: Optional[str] = None
    request_id: Optional[str] = None
    traceback: Optional[str] = None

    @staticmethod
    def success_result(data, request_id):
        """
        Create a successful result.

        Args:
            data: The result data to return
            request_id: Unique execution identifier

        Returns:
            Result object with success=True
        """
        return Result(
            success=True,
            data=data,
            request_id=request_id
        )

    @staticmethod
    def error_result(
        message,
        request_id,
        error_type,
        user_message=None,
        traceback=None
    ):
        """
        Create an error result.

        Args:
            message: Technical error message
            request_id: Unique execution identifier
            error_type: Type/class of error
            user_message: User-friendly message (defaults to message)
            traceback: Full stack trace for unexpected errors

        Returns:
            Result object with success=False
        """
        return Result(
            success=False,
            error_message=message,
            error_type=error_type,
            user_message=user_message or message,
            request_id=request_id,
            traceback=traceback
        )
