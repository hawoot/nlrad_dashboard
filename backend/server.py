"""
Backend initialization and bootstrap.

Called once during application startup.
"""
from backend.adapters.logger import configure_root_logger
from backend.core.registry import get_registry
from backend.core.executor import get_executor


def initialize_backend():
    """
    Initialize backend infrastructure.

    Process:
    1. Configure logging
    2. Initialize registry
    3. Initialize executor
    """
    # Configure logging
    configure_root_logger()

    # Initialize registry
    registry = get_registry()
    print(f"Registered {len(registry.list_all_tools())} tools")

    # Initialize executor
    executor = get_executor()

    print("Backend initialization complete")
