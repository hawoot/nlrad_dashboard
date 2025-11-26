"""
Custom exception types for the dashboard application.

Error Hierarchy:
- ToolExecutionError: Base for expected errors
  - ParameterValidationError: Invalid input parameters
  - DataAccessError: Database/data source errors
  - BusinessLogicError: Domain rule violations
- ToolNotFoundError: Tool path doesn't exist
- UINotFoundError: Tool UI module not found
"""


class ToolExecutionError(Exception):
    """
    Base exception for expected errors during tool execution.

    These errors are "expected" in the sense that they represent
    known failure modes (bad input, data not found, etc.) rather
    than unexpected bugs.
    """
    def __init__(self, message, user_message=None):
        """
        Args:
            message: Detailed error message for logs
            user_message: User-friendly message for UI display.
                         If None, uses message.
        """
        super().__init__(message)
        self.user_message = user_message or message


class ToolNotFoundError(Exception):
    """Raised when a tool path doesn't exist in the registry."""
    pass


class ParameterValidationError(ToolExecutionError):
    """Raised when tool parameters are invalid."""
    pass


class DataAccessError(ToolExecutionError):
    """Raised when database or data source access fails."""
    pass


class BusinessLogicError(ToolExecutionError):
    """Raised when business rules are violated."""
    pass


class UINotFoundError(Exception):
    """Raised when a tool UI module cannot be found."""
    pass
