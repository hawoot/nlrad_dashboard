"""
Base tool interface and execution context.

All tools must inherit from BaseTool and implement the run() method.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any
import logging


@dataclass
class ExecutionContext:
    """
    Context for a single tool execution.

    Carries all the metadata and utilities needed during execution,
    allowing tools to focus on business logic.

    Attributes:
        request_id: Unique identifier for this execution (UUID)
        user: User who initiated the execution
        timestamp: When execution started
        tool_path: Full path of the tool (e.g., "RAD/ingestor/timeline")
        params: Input parameters provided by user
        logger: Pre-configured logger with context
    """
    request_id: str
    user: str
    timestamp: datetime
    tool_path: str
    params: Dict[str, Any]
    logger: logging.Logger


class BaseTool(ABC):
    """
    Abstract base class for all tools.

    Tools are the executable units that implement business functionality.
    They validate parameters, coordinate models, and return results.

    Class attributes:
        category: Tool category path (e.g., "RAD/ingestor")
        name: Tool name (e.g., "timeline")
        description: Human-readable description
    """

    category = None
    name = None
    description = None

    def __init__(self):
        """Initialize the tool."""
        if not self.category or not self.name:
            raise ValueError(
                f"Tool {self.__class__.__name__} must define "
                f"'category' and 'name' class attributes"
            )

    @abstractmethod
    def run(self, context, **params):
        """
        Execute the tool logic.

        Args:
            context: Execution context with logger, user, etc.
            **params: Tool-specific parameters

        Returns:
            Result data (plain Python objects: dicts, lists, DataFrames, etc.)

        Raises:
            ToolExecutionError: For expected errors (validation, data access, etc.)
            Exception: For unexpected errors (will be caught by executor)
        """
        pass

    @property
    def full_path(self):
        """
        Get the full tool path.

        Returns:
            Full path string (e.g., "RAD/ingestor/timeline")
        """
        return f"{self.category}/{self.name}"

    def __repr__(self):
        return f"{self.__class__.__name__}(path='{self.full_path}')"
